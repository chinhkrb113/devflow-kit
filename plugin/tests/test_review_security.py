"""Review routing and copied security-validator portability contracts."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
NODE = os.environ.get('NODE_BINARY') or shutil.which('node')


class ReviewSecurityTests(unittest.TestCase):
    def test_entries_and_local_links(self):
        for name in ('open-code-review','security-audit'):
            root=ROOT/'skills'/name
            self.assertEqual(len(list(root.rglob('SKILL.md'))),1)
            for file in root.rglob('*.md'):
                for link in re.findall(r'\]\(([^)]+)\)',file.read_text(encoding='utf-8')):
                    if ':' in link or link.startswith('#') or '<' in link:continue
                    self.assertTrue((file.parent/link.split('#')[0]).exists(),f'{file}: {link}')

    def test_direct_and_router_share_coordination(self):
        outer=(ROOT/'PORTABLE-SKILL.md').read_text(encoding='utf-8')
        for name in ('open-code-review','security-audit'):
            self.assertIn(f'bundle/skills/{name}/SKILL.md',outer)
            entry=(ROOT/'skills'/name/'SKILL.md').read_text(encoding='utf-8')
            self.assertIn('../devflow/references/review-security.md',entry)

    @unittest.skipUnless(NODE,'Node required for copied validator transport')
    def test_copied_stdin_validator_runs_without_original_location(self):
        with tempfile.TemporaryDirectory(prefix='devflow-security-') as tmp:
            dest=Path(tmp)/'copied skill'
            shutil.copytree(ROOT/'skills/security-audit',dest)
            for kind in ('findings','coverage'):
                p=subprocess.run([NODE,dest/'validate-stdin.cjs',kind],input='[]',text=True,
                                 capture_output=True,encoding='utf-8',cwd=tmp,timeout=15)
                self.assertEqual(p.returncode,0,p.stdout+p.stderr)
                self.assertTrue(json.loads(p.stdout)['ok'])

    @unittest.skipUnless(NODE,'Node required for input rejection')
    def test_invalid_record_is_not_a_successful_audit(self):
        p=subprocess.run([NODE,ROOT/'skills/security-audit/validate-stdin.cjs','findings'],
                         input='[{"verdict":"confirmed"}]',text=True,capture_output=True,encoding='utf-8',timeout=15)
        self.assertEqual(p.returncode,1,p.stdout+p.stderr)
        self.assertFalse(json.loads(p.stdout)['ok'])


if __name__ == '__main__':
    unittest.main()
