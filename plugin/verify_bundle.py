"""Verify the distributed bundle; missing prerequisites are incomplete, never PASS."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from bundle_files import check_tree

ROOT = Path(__file__).resolve().parent


def check_manifest():
    portable = ROOT.parent / 'PORTABLE-MANIFEST.json'
    outer = ''
    if portable.exists():
        record = json.loads(portable.read_text(encoding='utf-8'))
        base = ROOT.parent.resolve()
        if record.get('format') != 'devflow-kit-portable-v1':
            raise ValueError('Invalid portable manifest format.')
        for name, digest in record['sha256'].items():
            p = (base / name).resolve()
            if not p.is_relative_to(base) or not p.is_file():
                raise ValueError('Invalid/missing portable file: ' + name)
            if hashlib.sha256(p.read_bytes()).hexdigest() != digest:
                raise ValueError('Portable file changed: ' + name)
        outer = f"Verified {len(record['sha256'])} portable file hashes. "
        check_tree(base, {*record['sha256'], 'PORTABLE-MANIFEST.json'})
    path = ROOT / 'RELEASE-MANIFEST.json'
    if not path.exists():
        return 'Source checkout: release manifest absent; archive integrity not checked.'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    for name, digest in manifest['sha256'].items():
        target = (ROOT / name).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            raise ValueError('Invalid/missing release file: ' + name)
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError('Release file changed: ' + name)
    check_tree(ROOT, {*manifest['sha256'], 'RELEASE-MANIFEST.json'}, prefix='bundle/')
    return outer + f"Verified {len(manifest['sha256'])} release file hashes."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--node', default=os.environ.get('NODE_BINARY', 'node'))
    parser.add_argument('--with-example', action='store_true')
    parser.add_argument('--playwright-module', default=os.environ.get('PLAYWRIGHT_MODULE'))
    parser.add_argument('--report', default=str(ROOT / 'verification-report.json'))
    args = parser.parse_args()
    report = {'started': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'checks': [],
              'scope': 'Bundle runtime checks' + (' and isolated example lifecycle' if args.with_example else ''),
              'result': 'incomplete'}
    exit_code = 2
    try:
        report['integrity'] = check_manifest()
        if sys.version_info < (3, 12):
            raise ValueError('Use Python 3.12+ for this verified distribution.')
        node = shutil.which(args.node)
        if not node:
            raise ValueError('Node executable not found: ' + args.node)
        version = subprocess.check_output([node, '--version'], text=True, timeout=10).strip()
        if not re.fullmatch(r'v\d+\.\d+\.\d+', version) or int(version[1:].split('.')[0]) < 22:
            raise ValueError('Use Node.js 22+ for the full bundle, found ' + version)
        if not shutil.which('git'):
            raise ValueError('Git is required for isolated clone regression tests.')
        report['runtime'] = {'python': sys.version.split()[0], 'node': version, 'platform': sys.platform}
        env = dict(os.environ, NODE_BINARY=node, PYTHONDONTWRITEBYTECODE='1')
        def run(name, command, cwd, timeout=180):
            p = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                               text=True, encoding='utf-8', timeout=timeout)
            report['checks'].append({'name': name, 'exit_code': p.returncode,
                                     'stdout': p.stdout, 'stderr': p.stderr})
            print(f'{name}: exit {p.returncode}', flush=True)
            if p.returncode:
                raise RuntimeError(name + ' failed; see report for output.')
        # One discovery command cannot recurse into unrelated test directories reliably.
        # Load each known suite and reject skips explicitly.
        code = (
            "import sys,unittest; "
            "suite=unittest.defaultTestLoader.discover(sys.argv[1]); "
            "r=unittest.TextTestRunner(verbosity=2).run(suite); "
            "sys.exit(0 if r.wasSuccessful() and not r.skipped else 1)"
        )
        run('bundle-tests', [sys.executable, '-X', 'utf8', '-c', code, 'tests'], ROOT)
        run('catalog-helper-tests', [sys.executable, '-X', 'utf8', '-c', code,
                                   'skills/devflow/tests'], ROOT)
        # Upstream file-reader cases declare OS capability skips; report them,
        # while portable stdin transport and schema tests must actually run.
        run('security-audit-validator-tests', [node, '--test', '--test-reporter=tap',
            'skills/security-audit/validate-findings.test.cjs',
            'skills/security-audit/validate-coverage-ledger.test.cjs',
            'skills/security-audit/validate-stdin.test.cjs'], ROOT)
        output = report['checks'][-1]['stdout']
        report['security_validator_counts'] = {
            key: int(re.search(r'^# ' + key + r' (\d+)$', output, re.M).group(1))
            for key in ('tests', 'pass', 'fail', 'skipped')}
        if report['security_validator_counts']['skipped']:
            report['capability_limits'] = ['Some upstream security file-reader tests require OS capabilities unavailable on this host; see explicit TAP skips. Stdin transport is tested separately.']
        if args.with_example:
            example = ROOT / 'examples/appointment-demo'
            module = args.playwright_module or 'playwright'
            # Check the browser too, before claiming example verification started.
            env['PLAYWRIGHT_MODULE'] = module
            run('example-browser-preflight', [node, '-e',
                "(async()=>{const {chromium}=require(process.env.PLAYWRIGHT_MODULE);"
                "const b=await chromium.launch({headless:true});await b.close()})()"
                ".catch(e=>{console.error(e.message);process.exitCode=1})"], example)
            run('example-lifecycle', [sys.executable, '-X', 'utf8', 'verify.py',
                                     '--node', node, '--playwright-module', module], example, 300)
        # Running the shipped example must not make a clean installation invalid.
        report['post_run_integrity'] = check_manifest()
        report['result'] = 'pass'
        report['not_executed'] = ['Codex activation, human acceptance, deployment',
                                 'Taste browser inspector (use the documented command on a running UI)']
        if not args.with_example:
            report['not_executed'].append('Appointment example browser/backend acceptance')
        exit_code = 0
    except (ValueError, OSError, subprocess.SubprocessError, KeyError) as exc:
        report['error'] = str(exc)
    except RuntimeError as exc:
        report['result'] = 'fail'
        report['error'] = str(exc)
        exit_code = 1
    destination = Path(args.report).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(report['result'].upper() + ': ' + str(destination))
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
