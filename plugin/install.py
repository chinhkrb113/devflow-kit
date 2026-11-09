"""Copy the self-contained skill to a harness; never replace existing content."""
import argparse
import json
import os
from pathlib import Path
import sys

from bundle_files import portable_files, check_tree

ROOT = Path(__file__).resolve().parent
NAME = 'devflow'
TARGETS = {'codex': '.agents', 'claude-code': '.claude', 'dsh': '.dsh',
           'trae': '.trae', 'trae-cn': '.trae'}


def destination(args):
    if args.skills_root:
        if args.target != 'generic':
            raise ValueError('--skills-root requires --target generic.')
        skills_root = Path(args.skills_root).expanduser().absolute()
    else:
        if args.target == 'generic':
            raise ValueError('--target generic requires --skills-root from your harness documentation.')
        if args.scope == 'project':
            project = Path(args.project).expanduser().absolute()
            if not project.is_dir():
                raise ValueError('--project must be an existing project directory.')
            config_root = project / TARGETS[args.target]
        else:
            # Respect documented custom config homes without printing their contents.
            override = {'claude-code': 'CLAUDE_CONFIG_DIR', 'dsh': 'DSH_HOME'}.get(args.target)
            configured = os.environ.get(override, '').strip() if override else ''
            folder = '.trae-cn' if args.target == 'trae-cn' else TARGETS[args.target]
            config_root = Path(configured).expanduser().absolute() if configured else Path.home() / folder
        skills_root = config_root / 'skills'
    if skills_root.is_dir():
        legacy = [p.name for p in skills_root.iterdir()
                  if p.name in {'reverse-engineered', 'find-reverse-engineered'}
                  or p.name.startswith('reverse-engineered-')]
        if legacy:
            raise ValueError('Legacy installation in this skills root: ' + ', '.join(sorted(legacy)) +
                             '. Archive the verified old bundle outside discovery before installing DevFlow Kit; nothing changed.')
    dest = skills_root / NAME
    # Refuse an alias to the source; copying inside the source would recursively package installs.
    own_capsule = ROOT.name == 'bundle' and dest.exists() and dest.resolve() == ROOT.parent.resolve()
    if not own_capsule and (dest.resolve().is_relative_to(ROOT.resolve()) or ROOT.resolve().is_relative_to(dest.resolve())):
        raise ValueError('Install destination overlaps the source bundle.')
    return dest


def verify_existing(dest, files):
    if dest.is_symlink() or (hasattr(dest, 'is_junction') and dest.is_junction()) or not dest.is_dir():
        raise ValueError('Destination is not a regular installation directory; nothing overwritten.')
    check_tree(dest, files)
    for name, data in files.items():
        p = dest / name
        if not p.resolve().is_relative_to(dest.resolve()) or not p.is_file() or p.read_bytes() != data:
            raise ValueError('Existing installation differs: ' + name + '; nothing overwritten.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True, choices=[*TARGETS, 'generic'])
    parser.add_argument('--scope', choices=['project', 'user'], default='project')
    parser.add_argument('--project', default=str(Path.cwd()))
    parser.add_argument('--skills-root', help='Exact skills root for an unlisted harness; appends devflow.')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--check', action='store_true', help='Verify installed files without writing.')
    args = parser.parse_args(argv)
    try:
        files = portable_files(ROOT)
        dest = destination(args)
        exists = os.path.lexists(dest)
        if exists:
            verify_existing(dest, files)
            status = 'already-installed'
        elif args.check:
            raise ValueError('Installation not found: ' + str(dest))
        else:
            status = 'planned' if args.dry_run else 'installed'
            if not args.dry_run:
                # Exclusive mkdir also rejects an installation racing this process.
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.mkdir()
                for name, data in files.items():
                    p = dest / name
                    p.parent.mkdir(parents=True, exist_ok=True)
                    with p.open('xb') as f:
                        f.write(data)
                verify_existing(dest, files)
        print(json.dumps(dict(status=status, target=args.target, destination=str(dest),
                              files=len(files), skill=NAME,
                              components=sum(n.startswith('bundle/skills/') and n.endswith('/SKILL.md') for n in files),
                              activation='not-tested-by-installer'), ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print('Installation failed: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
