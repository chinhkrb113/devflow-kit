import concurrent.futures
import http.client
import json
import sqlite3
import tempfile
import threading
import unittest
from contextlib import closing
from datetime import datetime
from unittest.mock import patch
from pathlib import Path

from server import create_server


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / 'test.sqlite3'
        self.start()

    def start(self):
        self.server = create_server(self.db, 0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def tearDown(self):
        self.stop()
        self.tmp.cleanup()

    def request(self, method, path, body=None, token='demo-an', raw=None, extra=None):
        conn = http.client.HTTPConnection('127.0.0.1', self.port, timeout=8)
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = 'Bearer ' + token
        headers.update(extra or {})
        data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
        try:
            conn.request(method, path, body=data, headers=headers)
            r = conn.getresponse()
            payload = r.read()
            return r.status, json.loads(payload) if r.getheader('Content-Type', '').startswith('application/json') else payload
        finally:
            conn.close()

    def book(self, **fields):
        return self.request('POST', '/api/bookings', {'date': '2030-11-04', 'slot': '09:00', 'note': 'Nội dung mẫu', **fields})

    def test_create_and_own_list(self):
        code, data = self.book()
        self.assertEqual(code, 201)
        self.assertEqual(set(data['booking']), {'id', 'date', 'slot', 'note', 'status'})
        code, data = self.request('GET', '/api/bookings')
        self.assertEqual(len(data['bookings']), 1)
        self.assertEqual(data['bookings'][0]['note'], 'Nội dung mẫu')

    def test_conflict_and_simultaneous_booking(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            codes = list(pool.map(lambda _: self.book()[0], range(6)))
        self.assertEqual(sorted(codes), [201, 409, 409, 409, 409, 409])
        self.assertEqual(len(self.request('GET', '/api/bookings')[1]['bookings']), 1)

    def test_auth_and_cross_owner_cancel(self):
        row = self.book()[1]['booking']
        for token in [None, 'incorrect']:
            self.assertEqual(self.request('GET', '/api/bookings', token=token)[0], 401)
        self.assertEqual(self.request('GET', '/api/bookings', token='demo-binh')[1]['bookings'], [])
        self.assertEqual(self.request('POST', f"/api/bookings/{row['id']}/cancel", {}, token='demo-binh')[0], 403)
        self.assertEqual(self.request('GET', '/api/bookings')[1]['bookings'][0]['status'], 'active')

    def test_cancel_idempotence_and_rebook(self):
        row = self.book()[1]['booking']
        path = f"/api/bookings/{row['id']}/cancel"
        self.assertEqual(self.request('POST', path, {})[0], 200)
        self.assertEqual(self.request('POST', path, {})[0], 200)
        self.assertEqual(self.request('POST', '/api/bookings', {'date': '2030-11-04', 'slot': '09:00', 'note': 'Bình đặt lại'}, token='demo-binh')[0], 201)
        self.assertEqual(len(self.request('GET', '/api/bookings', token='demo-binh')[1]['bookings']), 1)
        self.assertEqual(self.request('POST', '/api/bookings/not-found/cancel', {})[0], 404)

    def test_validation_rejects_without_writing(self):
        cases = [{'note': ''}, {'note': '   '}, {'note': 'x'*81}, {'note': None}, {'date': '2000-01-01'}, {'date': '20301104'}, {'date': '2030-02-30'}, {'slot': '09:15'}, {'slot': 9}, {'owner': 'binh'}]
        for fields in cases:
            with self.subTest(fields=fields):
                self.assertEqual(self.book(**fields)[0], 400)
        self.assertEqual(self.request('GET', '/api/bookings')[1]['bookings'], [])

    def test_bad_json_media_origin_and_body_limit(self):
        for raw in [b'{', b'[]', b'null', b'"text"', b'\xff']:
            self.assertEqual(self.request('POST', '/api/bookings', raw=raw)[0], 400)
        self.assertEqual(self.request('POST', '/api/bookings', raw=b' '*4097)[0], 413)
        self.assertEqual(self.request('POST', '/api/bookings', {}, extra={'Content-Type': 'text/plain'})[0], 415)
        self.assertEqual(self.request('POST', '/api/bookings', {}, extra={'Origin': 'https://unrelated.example'})[0], 403)

    def test_availability_and_strict_date(self):
        self.book()
        code, data = self.request('GET', '/api/slots?date=2030-11-04')
        self.assertEqual(code, 200)
        self.assertEqual(len(data['slots']), 6)
        self.assertFalse(data['slots'][0]['available'])
        self.assertTrue(data['slots'][1]['available'])
        for date in ['bad', '20301104', '2000-01-01']:
            self.assertEqual(self.request('GET', '/api/slots?date='+date)[0], 400)

    def test_restart_retains_booking(self):
        row = self.book()[1]['booking']
        self.stop()
        self.start()
        self.assertEqual(self.request('GET', '/api/bookings')[1]['bookings'][0], row)

    def test_backup_restore_integrity(self):
        self.book()
        with closing(sqlite3.connect(self.db)) as src, closing(sqlite3.connect(Path(self.tmp.name)/'restore.sqlite3')) as dst:
            src.backup(dst)
            self.assertEqual(dst.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
            self.assertEqual(dst.execute('SELECT * FROM bookings').fetchall(), src.execute('SELECT * FROM bookings').fetchall())

    def test_private_files_and_invalid_host_not_served(self):
        for path in ['/server.py', '/test.sqlite3', '/../PROJECT.md', '/api/unknown']:
            self.assertEqual(self.request('GET', path)[0], 404)
        self.assertEqual(self.request('GET', '/', extra={'Host':'unrelated.example'})[0], 403)

    def test_invalid_unicode_returns_400_and_server_recovers(self):
        for note in ['\ud800', '\udfff']:
            self.assertEqual(self.book(note=note)[0], 400)
        self.assertEqual(self.book(note='Tư vấn 🌱')[0], 201)

    def test_same_day_elapsed_slots(self):
        class FrozenDateTime(datetime):
            @classmethod
            def now(cls, tz=None):
                return cls(2030, 11, 4, 9, 15, tzinfo=tz)
        with patch('server.datetime', FrozenDateTime):
            data = self.request('GET', '/api/slots?date=2030-11-04')[1]
            self.assertFalse(data['slots'][0]['available'])
            self.assertTrue(data['slots'][1]['available'])
            self.assertEqual(self.book(slot='09:00')[0], 400)
            self.assertEqual(self.book(slot='09:30')[0], 201)


if __name__ == '__main__':
    unittest.main(verbosity=2)
