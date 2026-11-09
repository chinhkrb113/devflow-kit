"""Portable packaging/runtime checks; no network or user-history writes."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / 'skills/ui-ux-pro-max/scripts'
TASTE = ROOT / 'skills/taste-skill/scripts'
NODE = os.environ.get('NODE_BINARY') or shutil.which('node')


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ui-bundle-')
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1',
                        TASTE_SKILL_HISTORY=str(self.work / 'history.json'))

    def run_tool(self, argv, code=0):
        p = subprocess.run([str(x) for x in argv], cwd=self.work,
                           env=self.env, capture_output=True, text=True,
                           encoding='utf-8', timeout=45)
        self.assertEqual(p.returncode, code, p.stdout + p.stderr)
        return p.stdout

    def search(self, *args, code=0):
        return self.run_tool([sys.executable, '-X', 'utf8', UI / 'search.py', *args], code)

    def test_pinned_resources_and_licenses(self):
        lock = json.loads((ROOT / 'third-party-skills.lock.json').read_text())
        self.assertEqual({s['folder'] for s in lock['skills']},
                         {'frontend-design', 'ui-ux-pro-max', 'taste-skill',
                          'ponytail', 'caveman', 'ui-taste', 'superpowers', 'diagram-design', 'open-code-review', 'security-audit'})
        for skill in lock['skills']:
            base = ROOT / 'skills' / skill['folder']
            if skill.get('source_type') == 'hosted-snapshot':
                self.assertRegex(skill['snapshot_sha256'], r'^[0-9a-f]{64}$')
                self.assertTrue(skill['source_url'].startswith('https://uizze.sh/'))
                aggregate = json.dumps(skill['sha256'], sort_keys=True, separators=(',', ':')).encode()
                self.assertEqual(hashlib.sha256(aggregate).hexdigest(), skill['snapshot_sha256'])
            else:
                self.assertRegex(skill['revision'], r'^[0-9a-f]{40}$')
            self.assertTrue(any(name.startswith('LICENSE') for name in skill['sha256']))
            for name, digest in skill['sha256'].items():
                p = (base / name).resolve()
                self.assertTrue(p.is_relative_to(base.resolve()))
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), digest, str(p))

    def test_new_skill_resources_and_links(self):
        for name in ('NOTICE', 'LICENSE-MIT', 'LICENSING.md'):
            self.assertTrue((ROOT / 'skills/caveman' / name).is_file())
        for folder in ('ponytail', 'caveman', 'ui-taste'):
            base = ROOT / 'skills' / folder
            self.assertTrue((base / 'SKILL.md').is_file())
            for p in base.rglob('*.md'):
                for target in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
                    if '://' in target or target.startswith('#'):
                        continue
                    self.assertTrue((p.parent / target.split('#')[0]).exists(), f'{p}: {target}')
        base = ROOT / 'skills/ui-taste'
        lock = json.loads((ROOT / 'third-party-skills.lock.json').read_text())
        record = next(s for s in lock['skills'] if s['folder'] == 'ui-taste')
        for line in (base / 'CHECKSUMS.sha256').read_text().splitlines():
            digest, name = line.split(maxsplit=1)
            name = name.lstrip('*')
            if name in record.get('upstream_sha256', {}):
                self.assertEqual(record['upstream_sha256'][name], digest)
                self.assertNotEqual(record['sha256'][name], digest)
            else:
                self.assertEqual(hashlib.sha256((base / name).read_bytes()).hexdigest(), digest)

    def test_ui_entries_share_policy_and_compact_taste_resources(self):
        policy = ROOT / 'skills/devflow/references/ui-task-policy.md'
        self.assertTrue(policy.is_file())
        for folder in ('frontend-design', 'ui-ux-pro-max', 'taste-skill', 'ui-taste'):
            p = ROOT / 'skills' / folder / 'SKILL.md'
            text = p.read_text(encoding='utf-8')
            links = re.findall(r'\]\(([^)]+)\)', text)
            self.assertTrue(any((p.parent / target).resolve() == policy.resolve() for target in links))
            for target in links:
                if '://' not in target and not target.startswith('#'):
                    self.assertTrue((p.parent / target.split('#')[0]).exists(), f'{p}: {target}')
        entry = (ROOT / 'skills/taste-skill/SKILL.md').read_text(encoding='utf-8')
        self.assertLess(len(entry.split()), 700)
        self.assertTrue((ROOT / 'skills/taste-skill/references/full-workflow.md').is_file())

    @unittest.skipUnless(NODE, 'Node.js is needed for Uizze integrity tests')
    def test_uizze_evidence_rejects_missing_receipt(self):
        script = ROOT / 'skills/ui-taste/scripts/verify-visual-evidence.mjs'
        self.run_tool([NODE, '--check', script])
        result = json.loads(self.run_tool([NODE, script, self.work / 'missing.json'], code=1))
        self.assertFalse(result['ok'])

    @unittest.skipUnless(NODE, 'Node.js is needed for Uizze integrity tests')
    def test_uizze_verifier_runs_through_linked_install(self):
        # Installs may link the skill folder; the verifier must still run, not exit 0 silently.
        link = self.work / 'linked-ui-taste'
        target = ROOT / 'skills/ui-taste'
        if os.name == 'nt':
            import _winapi
            _winapi.CreateJunction(str(target), str(link))
        else:
            os.symlink(target, link, target_is_directory=True)
        out = self.run_tool([NODE, link / 'scripts/verify-visual-evidence.mjs', self.work / 'missing.json'], code=1)
        self.assertFalse(json.loads(out)['ok'])

    def test_vendored_shebang_scripts_use_lf(self):
        # '#!/usr/bin/env bash\r' cannot run on Linux/macOS; '-text' in .gitattributes ships bytes as-is.
        lock = json.loads((ROOT / 'third-party-skills.lock.json').read_text(encoding='utf-8'))
        for skill in lock['skills']:
            for p in (ROOT / 'skills' / skill['folder']).rglob('*'):
                if p.is_file() and '__pycache__' not in p.parts:
                    data = p.read_bytes()
                    if data.startswith(b'#!'):
                        self.assertNotIn(b'\r\n', data, str(p))

    def test_design_system_no_match_is_flagged_and_not_persisted(self):
        out = self.work / 'design'
        result = json.loads(self.search('zzzz qqqq', '--design-system', '--json', '--persist',
                                        '--output-dir', str(out)))
        self.assertTrue(result['design_system']['no_match_warning'])
        self.assertEqual(result['persistence']['status'], 'skipped_no_match')
        self.assertFalse(out.exists())
        self.assertIn('WARNING: No product category matched', self.search('zzzz qqqq', '--design-system'))
        matched = json.loads(self.search('SaaS dashboard', '--design-system', '--json'))
        self.assertIsNone(matched['design_system']['no_match_warning'])

    @unittest.skipUnless(NODE, 'Node.js is needed for Uizze integrity tests')
    def test_uizze_evidence_integrity_and_native_boundary(self):
        # Synthetic fixture exercises the validator, not a claim of visual inspection.
        import base64
        source = self.work / 'source.css'
        source.write_text('body { color: black; }')
        capture = self.work / 'fixture.png'
        capture.write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aK1sAAAAASUVORK5CYII='))
        def artifact(p, **extra):
            return dict(path=p.name, sha256=hashlib.sha256(p.read_bytes()).hexdigest(), **extra)
        receipt = dict(schemaVersion='uizze.visual-evidence.v1', scope='Validator fixture only',
                       platform='web', sources=[artifact(source)], comparison='existing-system',
                       requiredChecks=[dict(id='visual', kind='visual')], unresolved=[],
                       checks=[dict(id='visual', status='pass', state='fixture', observed='fixture',
                                    environment=dict(kind='browser', name='fixture', width=390, height=844),
                                    artifacts=[artifact(capture, kind='image')])])
        path = self.work / 'receipt.json'
        script = ROOT / 'skills/ui-taste/scripts/verify-visual-evidence.mjs'
        def check(code):
            path.write_text(json.dumps(receipt), encoding='utf-8')
            return json.loads(self.run_tool([NODE, script, path], code=code))
        self.assertTrue(check(0)['ok'])
        receipt['platform'] = 'ios'
        self.assertIn('native interface', ' '.join(check(1)['errors']))
        receipt['platform'] = 'web'
        source.write_text('body { color: red; }')
        self.assertIn('changed', ' '.join(check(1)['errors']))

    def test_integration_links(self):
        for p in [ROOT / 'INSTALL.md', ROOT / 'BAT-DAU.md', ROOT / 'THIRD_PARTY_NOTICES.md',
                  *list((ROOT / 'skills/devflow').rglob('*.md'))]:
            for target in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
                if '://' in target or target.startswith('#'):
                    continue
                self.assertTrue((p.parent / target.split('#')[0]).exists(), f'{p}: {target}')

    def test_search_paths_are_host_independent(self):
        text = (UI.parent / 'SKILL.md').read_text(encoding='utf-8')
        self.assertNotIn('CLAUDE_PLUGIN_ROOT', text)
        self.assertIn('<skill-root>/scripts/search.py', text)

    def test_missing_node_is_incomplete_not_pass(self):
        output = self.work / 'missing-node-report.json'
        self.run_tool([sys.executable, ROOT / 'verify_bundle.py', '--node',
                       str(self.work / 'missing-node'), '--report', output], code=2)
        report = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(report['result'], 'incomplete')
        self.assertEqual(report['checks'], [])
        self.assertIn('Node executable not found', report['error'])

    def test_demo_sources_are_portable(self):
        demo = ROOT / 'examples/appointment-demo'
        self.assertTrue((demo / 'server.py').is_file())
        self.assertTrue((demo / 'test_ui_states.cjs').is_file())
        # Inspect our shipped source, not dependencies installed by the recipient.
        # Playwright legitimately contains platform-specific Windows paths.
        for p in [*demo.glob('*.py'), *demo.glob('*.cjs'), *(demo / 'web').glob('*')]:
            if p.is_file() and p.suffix in ('.py', '.cjs', '.js', '.html', '.css'):
                self.assertNotRegex(p.read_text(encoding='utf-8-sig'), r'[CD]:[\\/]')

    def test_ux_search_from_unrelated_directory(self):
        result = json.loads(self.search('keyboard focus modal', '--domain', 'ux', '--json'))
        self.assertTrue(result['results'])

    def test_stack_search(self):
        result = json.loads(self.search('animate-pulse', '--stack', 'html-tailwind', '--json'))
        self.assertTrue(result['results'])

    def test_search_no_match_is_explicit(self):
        result = json.loads(self.search('zzzxxyy-no-such-guideline', '--stack', 'html-tailwind', '--json'))
        self.assertEqual(result['count'], 0)
        self.assertEqual(result['results'], [])

    def test_design_system_persistence_and_no_overwrite(self):
        args = ('appointment booking admin', '--design-system', '--json', '--persist',
                '--output-dir', str(self.work / 'design'), '-p', 'Bundle Test')
        result = json.loads(self.search(*args))
        self.assertTrue(result['design_system'])
        files = list((self.work / 'design').rglob('MASTER.md'))
        self.assertEqual(len(files), 1)
        files[0].write_text('owner-approved design', encoding='utf-8')
        second = json.loads(self.search(*args))
        self.assertEqual(second['persistence']['status'], 'skipped_exists')
        self.assertEqual(files[0].read_text(), 'owner-approved design')

    def test_invalid_search_domain(self):
        self.search('test', '--domain', 'not-a-domain', code=2)

    def test_data_integrity(self):
        self.run_tool([sys.executable, '-X', 'utf8', UI / 'validate_data.py'])

    @unittest.skipUnless(NODE, 'Node.js is needed for Taste runtime tests')
    def test_taste_javascript_syntax(self):
        for p in TASTE.parent.rglob('*'):
            if p.suffix in ('.mjs', '.js'):
                self.run_tool([NODE, '--check', p])

    @unittest.skipUnless(NODE, 'Node.js is needed for Taste runtime tests')
    def test_taste_app_draw_and_brand_preservation(self):
        args = [NODE, TASTE / 'draw.mjs', '--app', '--kind', 'smb-admin',
                '--brief', 'Appointment administration', '--keep', 'palette,type',
                '--seed', '17', '--out', self.work / 'app']
        self.run_tool([*args, '--options', '3'])
        self.assertFalse((self.work / 'app/direction.json').exists())
        self.run_tool(args)
        sheet = json.loads((self.work / 'app/direction.json').read_text(encoding='utf-8'))
        self.assertEqual(sheet['kind'], 'app')
        self.assertEqual(sheet['input']['keep'], ['palette', 'type'])
        self.assertTrue(sheet['screens'])
        self.run_tool([NODE, TASTE / 'draw.mjs', '--show', '--out', self.work / 'app'])

    @unittest.skipUnless(NODE, 'Node.js is needed for Taste runtime tests')
    def test_taste_site_draw(self):
        self.run_tool([NODE, TASTE / 'draw.mjs', '--sector', 'saas', '--brief',
                       'Appointment software overview', '--seed', '18', '--out', self.work / 'site'])
        sheet = json.loads((self.work / 'site/direction.json').read_text(encoding='utf-8'))
        self.assertTrue(sheet['direction']['id'])
        self.assertTrue(sheet['sections'])

    @unittest.skipUnless(NODE, 'Node.js is needed for Taste runtime tests')
    def test_taste_lint_exit_codes(self):
        p = self.work / 'sample.css'
        p.write_text('body { color: #112233; }', encoding='utf-8')
        json.loads(self.run_tool([NODE, TASTE / 'lint.mjs', p, '--app', '--json']))
        p.write_text('body { background: linear-gradient(red, blue); }', encoding='utf-8')
        json.loads(self.run_tool([NODE, TASTE / 'lint.mjs', p, '--app', '--json'], code=1))
        self.run_tool([NODE, TASTE / 'lint.mjs', self.work / 'missing.css'], code=2)


if __name__ == '__main__':
    unittest.main()
