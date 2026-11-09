"""Offline regression tests; all cache files, credentials and HTTP are isolated."""
import contextlib
import http.client
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 're_index.py'
spec = importlib.util.spec_from_file_location('skill_index', SCRIPT)
index = importlib.util.module_from_spec(spec)
spec.loader.exec_module(index)
ENTRY = {'name': 'Thiết bị 日本', 'url': 'https://github.com/owner/demo',
         'category': 'Devices', 'subcategory': 'Local', 'desc': 'Tuya local control',
         'stars': 100, 'lang': 'Python', 'archived': False, 'topics': ['local-control']}


class HelperTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.cache = self.root / 'cache' / 'entries.json'
        self.bundle = self.root / 'bundle.json'
        self.addCleanup(patch.stopall)
        patch.object(index, 'CACHE', str(self.cache)).start()
        patch.object(index, 'BUNDLED', str(self.bundle)).start()
        patch.dict(os.environ, {}, clear=True).start()
        self.http = patch.object(index.urllib.request, 'urlopen', side_effect=OSError('offline fixture')).start()
        self.git = patch.object(index.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, stdout='')).start()

    def write(self, path, entries=None, stale=False):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps([ENTRY] if entries is None else entries, ensure_ascii=False), encoding='utf-8')
        if stale:
            os.utime(path, (1, 1))

    def cli(self, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(sys, 'argv', ['re_index.py', *args]), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                code = index.main()
            except SystemExit as ex:
                code = ex.code
        return code, stdout.getvalue(), stderr.getvalue()

    def test_fresh_cache_avoids_network(self):
        self.write(self.cache)
        self.assertEqual(index.load(), [ENTRY])
        self.http.assert_not_called()

    def test_offline_bundle(self):
        self.write(self.bundle)
        self.assertEqual(index.load(), [ENTRY])

    def test_invalid_download_preserves_stale_cache(self):
        self.write(self.cache, stale=True)
        before = self.cache.read_bytes()
        self.http.side_effect = None
        self.http.return_value = io.BytesIO(b'<html>upstream error</html>')
        self.assertEqual(index.load(), [ENTRY])
        self.assertEqual(self.cache.read_bytes(), before)
        self.assertEqual(self.cache.stat().st_mtime, 1)

    def test_invalid_schema_does_not_replace_cache(self):
        self.write(self.cache, stale=True)
        before = self.cache.read_bytes()
        for value in ({'error': 'bad'}, [None], [{'name': 'incomplete'}], [dict(ENTRY, stars='100')], [dict(ENTRY, topics=[123])], [dict(ENTRY, desc=None)], [dict(ENTRY, url='owner/demo')]):
            with self.subTest(value=value):
                self.http.side_effect = None
                self.http.return_value = io.BytesIO(json.dumps(value).encode())
                self.assertEqual(index.load(), [ENTRY])
                self.assertEqual(self.cache.read_bytes(), before)

    def test_interrupted_http_read_preserves_stale_cache(self):
        self.write(self.cache, stale=True)
        self.http.side_effect = http.client.IncompleteRead(b'partial response')
        self.assertEqual(index.load(), [ENTRY])

    def test_atomic_cache_writes_never_expose_partial_json(self):
        self.write(self.cache)
        failures = []
        reads = []
        stop = threading.Event()
        def reader():
            while not stop.is_set():
                try:
                    data = json.loads(self.cache.read_text(encoding='utf-8'))
                    reads.append(True)
                    if data not in ([ENTRY], [dict(ENTRY, stars=200)]):
                        failures.append(data)
                except PermissionError as ex:
                    # Windows may briefly deny opening a file during replacement;
                    # this is not a partially written JSON document.
                    if os.name != 'nt':
                        failures.append(str(ex))
                except Exception as ex:
                    failures.append(str(ex))
        thread = threading.Thread(target=reader)
        thread.start()
        try:
            future = index.time.time() + 90000
            with patch.object(index.time, 'time', return_value=future):
                for i in range(12):
                    entries = [dict(ENTRY, stars=100 if i % 2 else 200)]
                    self.http.side_effect = None
                    self.http.return_value = io.BytesIO(json.dumps(entries).encode())
                    # Windows can refuse replacement while a reader holds the old file.
                    # The public loader must still return the valid download without data loss.
                    self.assertEqual(index.load(), entries)
        finally:
            stop.set()
            thread.join(timeout=5)
        self.assertFalse(thread.is_alive())
        self.assertTrue(reads)
        self.assertEqual(failures, [])
        self.assertEqual(list(self.cache.parent.iterdir()), [self.cache])

    def test_corrupt_cache_falls_back_to_bundle(self):
        self.cache.parent.mkdir()
        self.cache.write_text('{broken', encoding='utf-8')
        self.write(self.bundle)
        self.assertEqual(index.load(), [ENTRY])

    def test_corrupt_cache_can_be_repaired_by_valid_download(self):
        self.cache.parent.mkdir()
        self.cache.write_text('{broken', encoding='utf-8')
        self.http.side_effect = None
        self.http.return_value = io.BytesIO(json.dumps([ENTRY]).encode())
        self.assertEqual(index.load(), [ENTRY])
        self.assertEqual(json.loads(self.cache.read_text(encoding='utf-8')), [ENTRY])

    def test_cache_replace_failure_keeps_existing_bytes_and_cleans_temp(self):
        self.write(self.cache, stale=True)
        before = self.cache.read_bytes()
        new = [dict(ENTRY, stars=200)]
        self.http.side_effect = None
        self.http.return_value = io.BytesIO(json.dumps(new).encode())
        with patch.object(index.os, 'replace', side_effect=PermissionError('locked fixture')):
            self.assertEqual(index.load(), new)
        self.assertEqual(self.cache.read_bytes(), before)
        self.assertEqual(list(self.cache.parent.iterdir()), [self.cache])

    def test_explicit_invalid_override_fails_without_silent_fallback(self):
        self.write(self.bundle)
        bad = self.root / 'override.json'
        bad.write_text('{}', encoding='utf-8')
        os.environ['RE_INDEX_DATA'] = str(bad)
        code, _, err = self.cli('categories')
        self.assertEqual(code, 1)
        self.assertIn('error:', err)
        self.http.assert_not_called()

    def test_no_data_is_operational_failure(self):
        code, _, err = self.cli('categories')
        self.assertEqual(code, 1)
        self.assertIn('error:', err)

    def test_find_supported_reference_forms(self):
        for ref in ['owner/demo', 'https://github.com/OWNER/DEMO.git/', 'github.com/owner/demo', 'https://www.github.com/owner/demo']:
            with self.subTest(ref=ref):
                self.assertEqual(index.find([ENTRY], ref), ENTRY)

    def test_find_preserves_non_github_host_and_path_case(self):
        for url in ['https://gitlab.freedesktop.org/Owner/Project', 'https://git.sr.ht/~user/repo', 'https://gitdab.com/cadence/breezewiki']:
            entry = dict(ENTRY, url=url)
            with self.subTest(url=url):
                self.assertEqual(index.find([entry], url), entry)
                self.assertEqual(index.find([entry], url.removeprefix('https://')), entry)
        self.assertIsNone(index.find([dict(ENTRY, url='https://host.test/Upper')], 'https://host.test/upper'))

    def test_find_does_not_merge_distinct_query_resources(self):
        entry = dict(ENTRY, url='https://host.test/project?id=1')
        self.assertEqual(index.find([entry], entry['url']), entry)
        self.assertIsNone(index.find([entry], 'https://host.test/project?id=2'))

    def test_info_success(self):
        self.write(self.cache)
        self.http.side_effect = None
        self.http.return_value = io.BytesIO('README 日本\nsecond line'.encode())
        code, out, err = self.cli('info', 'owner/demo', '--lines', '1')
        self.assertEqual(code, 0)
        self.assertIn('README 日本', out)
        self.assertNotIn('second line', out)
        self.assertEqual(err, '')

    def test_info_readme_failure_is_nonzero_not_readme_text(self):
        self.write(self.cache)
        code, out, err = self.cli('info', 'owner/demo')
        self.assertEqual(code, 1)
        self.assertIn('could not fetch README', err)
        self.assertNotIn('--- README', out)

    def test_non_github_info_reports_partial_and_retains_metadata(self):
        entry = dict(ENTRY, url='https://gitlab.freedesktop.org/owner/demo')
        self.write(self.cache, [entry])
        code, out, err = self.cli('info', entry['url'])
        self.assertEqual(code, 3)
        self.assertIn(entry['name'], out)
        self.assertNotIn('not in index', out)
        self.assertIn('README', err)
        self.http.assert_not_called()

    def test_metadata_only_does_not_fetch_readme(self):
        self.write(self.cache)
        code, _, _ = self.cli('info', 'owner/demo', '--lines', '0')
        self.assertEqual(code, 0)
        self.http.assert_not_called()
        self.git.assert_not_called()

    def test_missing_metadata_only_is_partial(self):
        self.write(self.cache)
        code, _, _ = self.cli('info', 'owner/missing', '--lines', '0')
        self.assertEqual(code, 3)

    def test_argument_errors_do_not_fetch_data(self):
        for args in [('search', 'demo', '--limit', '0'), ('search', 'demo', '--min-stars', '-1'), ('search', '   '), ('info', 'owner/demo', '--lines', '-1'), ('info', 'file:///tmp/repo'), ('clone', '--upload-pack=bad'), ('info', 'https://user:password@github.com/owner/demo')]:
            with self.subTest(args=args):
                code, _, _ = self.cli(*args)
                self.assertEqual(code, 2)
        self.http.assert_not_called()

    def test_search_filter_and_empty_results(self):
        self.write(self.cache, [ENTRY, dict(ENTRY, name='Archived', archived=True)])
        code, out, err = self.cli('search', 'tuya', '--lang', 'Python', '--min-stars', '100', '--json')
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), [ENTRY])
        code, out, _ = self.cli('search', 'zzzznomatch', '--json')
        self.assertEqual((code, json.loads(out)), (0, []))

    def test_empty_dataset_is_valid(self):
        self.write(self.cache, [])
        code, out, _ = self.cli('categories')
        self.assertEqual((code, out), (0, ''))

    def test_clone_failure_has_nonzero_status(self):
        self.write(self.cache)
        self.git.side_effect = subprocess.CalledProcessError(128, ['git', 'clone'])
        code, out, err = self.cli('clone', 'owner/demo')
        self.assertEqual(code, 1)
        self.assertNotIn('cloned to', out)
        self.assertIn('error:', err)

    def test_clone_success(self):
        self.write(self.cache)
        code, out, _ = self.cli('clone', 'owner/demo', '--dest', 'vendor/demo')
        self.assertEqual(code, 0)
        self.assertIn('cloned to', out)
        self.assertEqual(self.git.call_args.args[0], ['git', 'clone', '--depth', '1', '--', ENTRY['url'], 'vendor/demo'])

    def test_clone_default_dest_is_outside_the_project(self):
        self.write(self.cache)
        code, _, err = self.cli('clone', 'owner/demo')
        self.assertEqual(code, 0)
        dest = self.git.call_args.args[0][-1]
        self.assertEqual(dest, os.path.join(os.path.dirname(str(self.cache)), 'clones', ENTRY['url'].rstrip('/').split('/')[-1]))
        self.assertIn('untrusted', err)


class SubprocessTests(unittest.TestCase):
    def test_unicode_file_and_output_without_utf8_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'entries.json'
            p.write_text(json.dumps([ENTRY], ensure_ascii=False), encoding='utf-8')
            env = dict(os.environ, RE_INDEX_DATA=str(p), PYTHONUTF8='0', PYTHONIOENCODING='cp1252', PYTHONDONTWRITEBYTECODE='1')
            run = subprocess.run([sys.executable, str(SCRIPT), 'search', 'tuya', '--json'], env=env, capture_output=True, timeout=20)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout.decode('utf-8')), [ENTRY])

    def test_cli_status_codes_in_real_process(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'entries.json'
            entry = dict(ENTRY, url='https://gitlab.freedesktop.org/owner/demo')
            p.write_text(json.dumps([entry]), encoding='utf-8')
            env = dict(os.environ, RE_INDEX_DATA=str(p), PYTHONDONTWRITEBYTECODE='1')
            for args, expected in [(['info', entry['url']], 3), (['info', entry['url'], '--lines', '0'], 0), (['search', 'demo', '--limit', '0'], 2)]:
                r = subprocess.run([sys.executable, str(SCRIPT), *args], env=env, capture_output=True, timeout=20)
                self.assertEqual(r.returncode, expected, r.stderr)
                self.assertNotIn(b'Traceback', r.stderr)
            p.write_text('{broken', encoding='utf-8')
            r = subprocess.run([sys.executable, str(SCRIPT), 'categories'], env=env, capture_output=True, timeout=20)
            self.assertEqual(r.returncode, 1)
            self.assertNotIn(b'Traceback', r.stderr)

    def test_clone_local_fixture_through_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, dest = root / 'source', root / 'checkout'
            env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_TERMINAL_PROMPT='0', PYTHONDONTWRITEBYTECODE='1')
            env.pop('GIT_CONFIG_COUNT', None)
            def git(*args):
                return subprocess.run(['git', *args], env=env, capture_output=True, check=True, timeout=20).stdout.decode().strip()
            git('-c', 'init.defaultBranch=main', 'init', str(source))
            (source / 'README.md').write_text('Harmless local skill test fixture.\n', encoding='utf-8')
            git('-C', str(source), 'add', 'README.md')
            git('-C', str(source), '-c', 'user.name=Skill Test', '-c', 'user.email=skill@example.invalid',
                '-c', 'commit.gpgsign=false', 'commit', '-m', 'fixture')
            expected = git('-C', str(source), 'rev-parse', 'HEAD')
            fixture_url = 'https://fixture.invalid/owner/repo'
            data = root / 'entries.json'
            data.write_text(json.dumps([dict(ENTRY, url=fixture_url)]), encoding='utf-8')
            env.update(RE_INDEX_DATA=str(data), GIT_CONFIG_COUNT='1',
                       GIT_CONFIG_KEY_0='url.' + source.as_uri() + '.insteadOf', GIT_CONFIG_VALUE_0=fixture_url)
            r = subprocess.run([sys.executable, str(SCRIPT), 'clone', fixture_url, '--dest', str(dest)], env=env, capture_output=True, timeout=30)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(git('-C', str(dest), 'rev-parse', 'HEAD'), expected)
            self.assertEqual((dest / 'README.md').read_text(), (source / 'README.md').read_text())


if __name__ == '__main__':
    unittest.main()
