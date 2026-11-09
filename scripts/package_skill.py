"""Create a clean distributable plugin ZIP plus file manifest and archive checksum."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1] / 'plugin'
sys.path.insert(0, str(ROOT))
from bundle_files import collect, hashes, portable_files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--format', choices=['plugin', 'portable'], default='portable')
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    source = collect(ROOT)
    version = json.loads(source['.claude-plugin/plugin.json'])['version']
    if args.format == 'portable':
        files = portable_files(ROOT)
        prefix = 'devflow/'
    else:
        files = source
        manifest = {'version': version, 'created_utc': datetime.now(timezone.utc).isoformat(),
                    'sha256': hashes(files)}
        files['RELEASE-MANIFEST.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
        prefix = 'plugin/'
    # Exclusive creation prevents silently replacing a handed-off archive.
    with zipfile.ZipFile(output, 'x', zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            archive.writestr(prefix + name, data)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + '.sha256').write_text(digest + '  ' + output.name + '\n', encoding='utf-8')
    print(json.dumps({'archive': str(output), 'version': version,
                      'format': args.format, 'files': len(files), 'bytes': output.stat().st_size, 'sha256': digest}, indent=2))


if __name__ == '__main__':
    main()
