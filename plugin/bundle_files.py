"""Single allowlist used by the release packager and portable installer."""
import hashlib
import json
import os
from pathlib import Path

TOP_FILES = {'.gitattributes', 'BAT-DAU.md', 'INSTALL.md', 'LICENSE',
             'THIRD_PARTY_NOTICES.md', 'RELEASE-NOTES.md', 'install-codex.ps1',
             'third-party-skills.lock.json', 'verify_bundle.py', 'install.py',
             'bundle_files.py', 'PORTABLE-SKILL.md', 'PORTABLE-START.md',
             'HARNESS-COMPATIBILITY.md'}
DEMO_FILES = {'README.md', 'package.json', 'server.py', 'verify.py', 'test_server.py',
              'test_browser.cjs', 'test_browser_races.cjs', 'test_ui_states.cjs',
              'api-contract.json', 'web/index.html', 'web/app.js', 'web/style.css'}
SKIP_DIRS = {'__pycache__', 'node_modules', '.git', 'evidence', '.taste-skill'}


def included(relative):
    if any(part in SKIP_DIRS for part in relative.parts) or relative.suffix in {'.pyc', '.pyo'}:
        return False
    if len(relative.parts) == 1:
        return relative.name in TOP_FILES
    if relative.parts[0] == 'examples':
        return (relative.parts[:2] == ('examples', 'appointment-demo') and
                Path(*relative.parts[2:]).as_posix() in DEMO_FILES)
    return relative.parts[0] in {'skills', 'tests', '.claude-plugin'}


def hashes(files):
    return {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}


def runtime_output(name):
    """Explicit non-source outputs; never ignore whole runtime directories."""
    p = Path(name)
    if name == 'bundle/verification-report.json':
        return True
    if p.parent.as_posix() == 'bundle/examples/appointment-demo/evidence':
        return p.suffix in {'.json', '.log', '.png', '.webm', '.mp4'}
    if p.parent.as_posix() == 'bundle/examples/appointment-demo/evidence/ui-redesign':
        return p.name in {'ui-states.json', 'mock-320.png', 'mock-390.png',
                          'mock-768.png', 'mock-1440.png'}
    return (p.parts[0] == 'bundle' and p.parent.name == '__pycache__'
            and p.suffix == '.pyc')


def check_tree(root, expected, prefix=''):
    """Reject unlisted payloads and links, without deleting or following them."""
    expected = set(expected)
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            p = Path(directory) / name
            relative = p.relative_to(root).as_posix()
            if p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()):
                raise ValueError('Linked installation path: ' + relative)
            if name in files and relative not in expected and not runtime_output(prefix + relative):
                raise ValueError('Unexpected installation file: ' + relative)


def collect(root):
    root = root.resolve()
    files = {}
    for p in sorted(root.rglob('*')):
        relative = p.relative_to(root)
        if p.is_file() and included(relative):
            if not p.resolve().is_relative_to(root):
                raise ValueError('External linked file: ' + str(p))
            files[relative.as_posix()] = p.read_bytes()
    missing = TOP_FILES - files.keys()
    if missing:
        raise ValueError('Missing bundle files: ' + ', '.join(sorted(missing)))
    manifest = root / 'RELEASE-MANIFEST.json'
    if manifest.exists():
        recorded = json.loads(manifest.read_text(encoding='utf-8'))['sha256']
        check_tree(root, {*recorded, 'RELEASE-MANIFEST.json'}, prefix='bundle/')
        if recorded != hashes(files):
            raise ValueError('Release manifest mismatch; use an intact extracted archive.')
    return files


def portable_files(root):
    files = collect(root)
    version = json.loads(files['.claude-plugin/plugin.json'])['version']
    release = dict(version=version, sha256=hashes(files))
    payload = {'SKILL.md': files['PORTABLE-SKILL.md'], 'START-HERE.md': files['PORTABLE-START.md']}
    payload.update({'bundle/' + name: data for name, data in files.items()})
    payload['bundle/RELEASE-MANIFEST.json'] = (json.dumps(release, indent=2) + '\n').encode()
    manifest = dict(format='devflow-kit-portable-v1', version=version, sha256=hashes(payload))
    payload['PORTABLE-MANIFEST.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    return payload
