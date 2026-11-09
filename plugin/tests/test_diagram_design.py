"""Exercise the shipped diagram helpers from a copied, standalone component."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills/diagram-design'


class DiagramDesignTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='devflow-diagram-')
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)
        self.skill = self.work / 'copied skill'
        shutil.copytree(SOURCE, self.skill, ignore=shutil.ignore_patterns('__pycache__'))

    def run_helper(self, name, *args, code=0):
        result = subprocess.run([sys.executable, '-X', 'utf8', self.skill / 'scripts' / name, *map(str,args)],
                                cwd=self.work, capture_output=True, text=True, encoding='utf-8', timeout=30)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result.stdout

    def fixture(self, body=''):
        p = self.work / 'sample.html'
        p.write_text('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Sample</title></head><body>'
                     '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-labelledby="sample-title sample-desc">'
                     '<title id="sample-title">Sample</title><desc id="sample-desc">A component sends data to another.</desc>'
                     + body + '</svg></body></html>', encoding='utf-8')
        return p

    def test_entry_routes_to_packaged_resources(self):
        for p in [self.skill/'SKILL.md', self.skill/'references/devflow-integration.md']:
            for link in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
                if '://' in link or link.startswith('#') or link.startswith('../devflow/'):continue
                self.assertTrue((p.parent/link.split('#')[0]).exists(),link)
        self.assertEqual(len(list(SOURCE.rglob('SKILL.md'))),1)
        outer=(ROOT/'PORTABLE-SKILL.md').read_text(encoding='utf-8')
        self.assertIn('bundle/skills/diagram-design/SKILL.md',outer)

    def test_offline_structural_check(self):
        self.run_helper('self_check.py','--offline',self.fixture())

    def test_structural_check_rejects_missing_accessibility(self):
        p=self.fixture();p.write_text(p.read_text().replace('role="img"',''),encoding='utf-8')
        self.run_helper('self_check.py',p,code=1)

    def test_geometry_rejects_diagonal_connector(self):
        p=self.fixture('<defs><marker id="a"/></defs><path d="M20 20 L200 150" marker-end="url(#a)"/>')
        output=self.run_helper('verify_geometry.py',p,code=1)
        self.assertIn('sample.html',output)

    def test_geometry_accepts_orthogonal_connector(self):
        self.run_helper('verify_geometry.py',self.fixture('<defs><marker id="a"/></defs><path d="M20 20 H200" marker-end="url(#a)"/>'))

    def test_svg_export_preserves_accessibility(self):
        target=self.work/'export.svg'
        self.run_helper('export_svg.py',self.fixture(),target)
        output=target.read_text(encoding='utf-8')
        self.assertIn('sample-title',output)
        self.assertIn('sample-desc',output)
        self.assertNotIn('<html',output)


if __name__ == '__main__':
    unittest.main()
