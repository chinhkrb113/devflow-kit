"""Release identity must survive copying and component routing."""
import json
from pathlib import Path
import sys
import tempfile
import argparse
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bundle_files import portable_files
import install


class BrandingTests(unittest.TestCase):
    def test_devflow_identity_and_router(self):
        files = portable_files(ROOT)
        self.assertIn(b'\nname: devflow\n', files['SKILL.md'])
        self.assertEqual(install.NAME, 'devflow')
        plugin = json.loads(files['bundle/.claude-plugin/plugin.json'])
        self.assertEqual(plugin['name'], 'devflow-kit')
        self.assertEqual(json.loads(files['PORTABLE-MANIFEST.json'])['format'], 'devflow-kit-portable-v1')
        self.assertIn('bundle/skills/devflow/SKILL.md', files)
        self.assertNotIn('bundle/skills/find-reverse-engineered/SKILL.md', files)
        self.assertIn(b'$devflow ', files['bundle/skills/devflow/agents/openai.yaml'])

    def test_legacy_install_is_preserved_and_requires_migration(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('reverse-engineered', 'find-reverse-engineered', 'reverse-engineered-frontend-design'):
                old = root / name
                old.mkdir()
                marker = old / 'SKILL.md'
                marker.write_text('previous installation')
                args = argparse.Namespace(target='generic', skills_root=str(root))
                with self.assertRaisesRegex(ValueError, 'Legacy installation'):
                    install.destination(args)
                self.assertEqual(marker.read_text(), 'previous installation')
                self.assertFalse((root / 'devflow').exists())
                marker.unlink()
                old.rmdir()


if __name__ == '__main__':
    unittest.main()
