"""Repeatable local acceptance: isolated DBs, real HTTP/browser, restart and restore."""
import argparse
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from contextlib import closing
from pathlib import Path
from server import create_server

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'evidence'


def read_bookings(port):
    request = urllib.request.Request(f'http://127.0.0.1:{port}/api/bookings', headers={'Authorization': 'Bearer demo-an'})
    with urllib.request.urlopen(request, timeout=8) as response:
        return json.load(response)['bookings']


def check_contract():
    contract = json.loads((ROOT/'api-contract.json').read_text(encoding='utf-8'))
    assert contract['version'] == '1.0'
    assert len(contract['slots']) == 6 and len(set(contract['slots'])) == 6
    expected = {'GET /api/slots?date=YYYY-MM-DD', 'GET /api/bookings', 'POST /api/bookings', 'POST /api/bookings/{id}/cancel'}
    assert set(contract['routes']) == expected
    for route in contract['routes'].values():
        assert route['auth'] is True and isinstance(route['response'], dict)
        assert route['status'] and all(isinstance(code,int) and 200 <= code <= 599 for code in route['status'])
    return 'Custom contract syntax/required fields checked; HTTP behavior tested separately. Not an OpenAPI validator.'


def start_server(db):
    server = create_server(db, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def stop_server(pair):
    server, thread = pair
    server.shutdown(); server.server_close(); thread.join()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--node', default='node')
    parser.add_argument('--playwright-module')
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    report = {'started': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'checks': [], 'python': sys.version, 'scope': 'Local technical acceptance only; human sign-off and release unverified'}
    env = dict(os.environ)
    if args.playwright_module:
        env['PLAYWRIGHT_MODULE'] = args.playwright_module
    def run(name, command):
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8', timeout=120)
        (OUT/(name+'.log')).write_text(result.stdout+result.stderr, encoding='utf-8')
        report['checks'].append({'name':name,'command':command,'exit_code':result.returncode})
        if result.returncode:
            raise RuntimeError(name+' failed; see evidence/'+name+'.log')
    try:
        report['contract'] = check_contract()
        run('backend-tests', [sys.executable, '-X', 'utf8', '-m', 'unittest', '-v', 'test_server'])
        with tempfile.TemporaryDirectory(prefix='skill-flow-verify-') as temp:
            db = Path(temp)/'bookings.sqlite3'
            pair = start_server(db)
            try:
                port = pair[0].server_port
                run('prototype-run', [args.node, str(ROOT/'test_browser.cjs'), f'http://127.0.0.1:{port}/?mock=1', 'prototype'])
                assert read_bookings(port) == [], 'Prototype unexpectedly wrote to real DB'
                run('system-run', [args.node, str(ROOT/'test_browser.cjs'), f'http://127.0.0.1:{port}/', 'system'])
                run('race-run', [args.node, str(ROOT/'test_browser_races.cjs'), f'http://127.0.0.1:{port}/'])
                run('ui-states-run', [args.node, str(ROOT/'test_ui_states.cjs'), f'http://127.0.0.1:{port}/'])
                before = read_bookings(port)
                assert len(before) == 1 and before[0]['status'] == 'cancelled'
                with closing(sqlite3.connect(db)) as connection:
                    count = connection.execute('SELECT count(*) FROM bookings').fetchone()[0]
                assert count == 1, 'Real UI did not persist expected SQLite row'
                report['storage'] = {'mock_wrote_db':False, 'real_ui_rows':count, 'status':before[0]['status']}
            finally:
                stop_server(pair)
            pair = start_server(db)
            try:
                assert read_bookings(pair[0].server_port) == before
                report['restart'] = 'Same SQLite rows returned through HTTP after server restart'
            finally:
                stop_server(pair)
            restored = Path(temp)/'restored.sqlite3'
            began = time.perf_counter()
            with closing(sqlite3.connect(db)) as src, closing(sqlite3.connect(restored)) as dst:
                src.backup(dst)
                assert dst.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
                assert dst.execute('SELECT * FROM bookings').fetchall() == src.execute('SELECT * FROM bookings').fetchall()
            pair = start_server(restored)
            try:
                assert read_bookings(pair[0].server_port) == before
                report['restore'] = {'verified':True,'seconds':round(time.perf_counter()-began,4),'scope':'one-row local fixture, not production RTO/RPO'}
            finally:
                stop_server(pair)
        report['result'] = 'pass'
    except Exception as exc:
        report['result'] = 'fail';report['error'] = str(exc)
    report['sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'server.py',ROOT/'test_server.py',ROOT/'test_browser.cjs',ROOT/'test_browser_races.cjs',ROOT/'test_ui_states.cjs',ROOT/'verify.py',ROOT/'api-contract.json',*sorted((ROOT/'web').glob('*'))]}
    (OUT/'acceptance.json').write_text(json.dumps(report, ensure_ascii=False, indent=2),encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['result']=='pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
