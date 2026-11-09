"""Portable delivery contract: copying, integrity and resource independence."""
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import argparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bundle_files import portable_files
import install as installer_module


class PortableTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='skill-portable-')
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name) / 'Dự án có dấu'
        self.work.mkdir()

    def invoke(self, *args, code=0, installer=None):
        result = subprocess.run([sys.executable, '-X', 'utf8', str(installer or ROOT / 'install.py'), *args],
                                capture_output=True, text=True, encoding='utf-8', timeout=40,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout) if code == 0 else result.stderr

    def test_all_target_copy_roots_and_idempotence(self):
        for target, folder in [('codex', '.agents'), ('claude-code', '.claude'),
                               ('dsh', '.dsh'), ('trae', '.trae'), ('trae-cn', '.trae')]:
            project = self.work / target
            project.mkdir()
            args = ['--target', target, '--project', str(project)]
            result = self.invoke(*args)
            dest = project / folder / 'skills/devflow'
            self.assertEqual(Path(result['destination']), dest)
            self.assertFalse(dest.is_symlink())
            self.assertFalse(dest.is_junction())
            self.assertTrue((dest / 'SKILL.md').is_file())
            self.assertEqual(result['components'], 11)
            self.assertEqual(self.invoke(*args)['status'], 'already-installed')
            self.invoke(*args, '--check')

    def test_generic_dry_run_writes_nothing(self):
        skills = self.work / 'custom skills'
        r = self.invoke('--target', 'generic', '--skills-root', str(skills), '--dry-run')
        self.assertEqual(r['status'], 'planned')
        self.assertFalse(skills.exists())
        self.invoke('--target', 'generic', code=2)
        self.invoke('--target', 'codex', '--skills-root', str(skills), code=2)
        self.invoke('--target', 'generic', '--skills-root', str(skills), '--check', code=2)

    def test_user_roots_and_custom_config_homes(self):
        with mock.patch.object(Path, 'home', return_value=self.work), mock.patch.dict(os.environ, {}, clear=True):
            for target, folder in [('codex', '.agents'), ('claude-code', '.claude'),
                                   ('dsh', '.dsh'), ('trae', '.trae'), ('trae-cn', '.trae-cn')]:
                args = argparse.Namespace(target=target, scope='user', project='unused', skills_root=None)
                self.assertEqual(installer_module.destination(args), self.work / folder / 'skills/devflow')
            for target, variable in [('claude-code', 'CLAUDE_CONFIG_DIR'), ('dsh', 'DSH_HOME')]:
                custom = self.work / (target + '-custom')
                with mock.patch.dict(os.environ, {variable: str(custom)}):
                    args = argparse.Namespace(target=target, scope='user', project='unused', skills_root=None)
                    self.assertEqual(installer_module.destination(args), custom / 'skills/devflow')

    def test_existing_content_is_not_overwritten(self):
        skills = self.work / 'skills'
        dest = skills / 'devflow'
        dest.mkdir(parents=True)
        (dest / 'SKILL.md').write_text('user-owned')
        self.invoke('--target', 'generic', '--skills-root', str(skills), code=2)
        self.assertEqual((dest / 'SKILL.md').read_text(), 'user-owned')
        self.assertEqual(len(list(dest.iterdir())), 1)

    def test_check_rejects_extra_skill_script_and_disguised_resource(self):
        skills = self.work / 'skills'
        args = ['--target', 'generic', '--skills-root', str(skills)]
        dest = Path(self.invoke(*args)['destination'])
        for name in ('bundle/skills/unexpected/SKILL.md', 'bundle/skills/ponytail/extra.py',
                     'bundle/examples/appointment-demo/evidence/SKILL.md',
                     'bundle/examples/appointment-demo/evidence/ui-redesign/SKILL.md',
                     'bundle/examples/appointment-demo/evidence/ui-redesign/extra.js',
                     'bundle/examples/appointment-demo/evidence/ui-redesign/unknown.png',
                     'bundle/__pycache__/extra.py', '.git/SKILL.md'):
            with self.subTest(name=name):
                extra = dest / name
                extra.parent.mkdir(parents=True, exist_ok=True)
                extra.write_text('harmless regression fixture', encoding='utf-8')
                error = self.invoke(*args, '--check', code=2)
                self.assertIn('Unexpected installation file', error)
                self.assertTrue(extra.exists(), 'Verifier must not delete user files')
                extra.unlink()

    def test_check_allows_only_documented_runtime_outputs(self):
        skills = self.work / 'skills'
        args = ['--target', 'generic', '--skills-root', str(skills)]
        dest = Path(self.invoke(*args)['destination'])
        for name in ('bundle/verification-report.json',
                     'bundle/examples/appointment-demo/evidence/backend-tests.log',
                     'bundle/examples/appointment-demo/evidence/system-desktop.png',
                     'bundle/examples/appointment-demo/evidence/ui-redesign/mock-1440.png',
                     'bundle/examples/appointment-demo/evidence/ui-redesign/ui-states.json',
                     'bundle/__pycache__/install.cpython-312.pyc'):
            p = dest / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b'fixture only')
        self.assertEqual(self.invoke(*args, '--check')['status'], 'already-installed')
        self.invoke(*args, '--check', installer=dest / 'bundle/install.py')

    def test_installed_copy_works_after_source_moves(self):
        # Build a temporary distribution and only rename this owned temporary tree.
        source = self.work / 'source'
        source.mkdir()
        for name, data in portable_files(ROOT).items():
            p = source / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        skills = self.work / 'skills'
        r = self.invoke('--target', 'generic', '--skills-root', str(skills),
                        installer=source / 'bundle/install.py')
        source.rename(self.work / 'moved-source')
        installed = Path(r['destination'])
        # The installed copy must also be able to verify/re-run its own installer.
        self.invoke('--target', 'generic', '--skills-root', str(skills), '--check',
                    installer=installed / 'bundle/install.py')
        self.assertEqual(self.invoke('--target', 'generic', '--skills-root', str(skills),
                                    installer=installed / 'bundle/install.py')['status'], 'already-installed')
        self.invoke('--target', 'generic', '--skills-root', str(skills), '--check',
                    installer=self.work / 'moved-source/bundle/install.py')
        p = subprocess.run([sys.executable, str(installed / 'bundle/skills/ui-ux-pro-max/scripts/search.py'),
                            'keyboard focus', '--domain', 'ux', '--json'], capture_output=True,
                           text=True, encoding='utf-8', timeout=30)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertTrue(json.loads(p.stdout)['results'])

    def test_modified_source_manifest_is_rejected(self):
        source = self.work / 'source'
        for name, data in portable_files(ROOT).items():
            p = source / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        (source / 'bundle/skills/ponytail/SKILL.md').write_text('tampered')
        skills = self.work / 'skills'
        self.invoke('--target', 'generic', '--skills-root', str(skills),
                    installer=source / 'bundle/install.py', code=2)
        self.assertFalse(skills.exists())

    def test_missing_source_file_and_overlap_are_rejected(self):
        self.invoke('--target', 'generic', '--skills-root', str(ROOT / 'inside'), code=2)
        source = self.work / 'source'
        for name, data in portable_files(ROOT).items():
            p = source / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        (source / 'bundle/skills/ponytail/SKILL.md').unlink()
        self.invoke('--target', 'generic', '--skills-root', str(self.work / 'skills'),
                    installer=source / 'bundle/install.py', code=2)

    def test_outer_entry_and_relative_links_are_self_contained(self):
        files = portable_files(ROOT)
        text = files['SKILL.md'].decode('utf-8')
        self.assertRegex(text, r'^---\nname: devflow\n')
        description = re.search(r'^description: (.+)$', text, re.M).group(1)
        self.assertLessEqual(len(description), 1024)
        for entry in ('SKILL.md', 'START-HERE.md'):
            for link in re.findall(r'\]\(([^)]+)\)', files[entry].decode('utf-8')):
                if '://' not in link and not link.startswith('#'):
                    self.assertIn(link.split('#')[0], files, link)
        self.assertEqual(sum(n.startswith('bundle/skills/') and n.endswith('/SKILL.md') for n in files), 11)

    def test_verifier_checks_outer_entry_and_path_traversal(self):
        source = self.work / 'source'
        for name, data in portable_files(ROOT).items():
            p = source / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        spec = importlib.util.spec_from_file_location('portable_verify', source / 'bundle/verify_bundle.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertIn('portable file hashes', module.check_manifest())
        extra = source / 'bundle/skills/extra/SKILL.md'
        extra.parent.mkdir()
        extra.write_text('fixture', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Unexpected installation file'):
            module.check_manifest()
        self.invoke('--target', 'generic', '--skills-root', str(self.work / 'extra-check'),
                    installer=source / 'bundle/install.py', code=2)
        self.assertFalse((self.work / 'extra-check').exists())
        extra.unlink()
        original = (source / 'SKILL.md').read_bytes()
        (source / 'SKILL.md').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'Portable file changed'):
            module.check_manifest()
        (source / 'SKILL.md').write_bytes(original)
        p = source / 'PORTABLE-MANIFEST.json'
        manifest = json.loads(p.read_text())
        manifest['sha256']['../outside.txt'] = '0' * 64
        p.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'Invalid/missing portable file'):
            module.check_manifest()

    def test_check_rejects_linked_directories(self):
        skills = self.work / 'skills'
        args = ['--target', 'generic', '--skills-root', str(skills)]
        dest = Path(self.invoke(*args)['destination'])
        outside = self.work / 'outside'
        outside.mkdir()
        link = dest / 'runtime-link'
        if os.name == 'nt':
            # Owned temporary junction, created and removed without shell deletion.
            command = ['powershell', '-NoProfile', '-Command',
                       'New-Item -ItemType Junction -Path $env:TEST_LINK -Target $env:TEST_TARGET | Out-Null']
            result = subprocess.run(command, capture_output=True, text=True,
                                    env=dict(os.environ, TEST_LINK=str(link), TEST_TARGET=str(outside)), timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            link.symlink_to(outside, target_is_directory=True)
        try:
            self.assertIn('Linked installation path', self.invoke(*args, '--check', code=2))
        finally:
            if os.name == 'nt':
                link.rmdir()  # Non-recursive removal of our temporary junction only.
            else:
                link.unlink()
        self.assertTrue(outside.is_dir())


if __name__ == '__main__':
    unittest.main()
