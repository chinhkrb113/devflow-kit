"""Loopback-only appointment fixture. Demo tokens are NOT production authentication."""
import argparse
import json
import re
import sqlite3
import uuid
from contextlib import closing
from datetime import date, datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent
TZ = timezone(timedelta(hours=7))
SLOTS = ('09:00', '09:30', '10:00', '10:30', '14:00', '14:30')
TOKENS = {'demo-an': 'an', 'demo-binh': 'binh'}
PUBLIC = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'application/javascript'), '/style.css': ('style.css', 'text/css')}


class ApiError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message


def valid_date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ApiError(400, 'Chọn ngày theo định dạng YYYY-MM-DD.')
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        raise ApiError(400, 'Ngày hẹn không hợp lệ.') from None
    if parsed < datetime.now(TZ).date():
        raise ApiError(400, 'Không thể đặt lịch cho ngày đã qua.')
    return value


def past(day, slot):
    return datetime.fromisoformat(f'{day}T{slot}:00+07:00') <= datetime.now(TZ)


def connect(path):
    db = sqlite3.connect(path, timeout=10)
    db.row_factory = sqlite3.Row
    return db


def public_row(row):
    return {k: row[k] for k in ('id', 'date', 'slot', 'note', 'status')}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # No tokens, bodies or user notes in access logs.
        pass

    def send(self, code, data, content_type='application/json'):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8') if content_type == 'application/json' else data
        self.send_response(code)
        self.send_header('Content-Type', content_type + '; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(body)

    def user(self):
        token = self.headers.get('Authorization', '')
        owner = TOKENS.get(token.removeprefix('Bearer ')) if token.startswith('Bearer ') else None
        if owner is None:
            raise ApiError(401, 'Chọn danh tính demo hợp lệ.')
        return owner

    def body(self):
        if self.headers.get_content_type() != 'application/json':
            raise ApiError(415, 'Yêu cầu phải dùng JSON.')
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            raise ApiError(400, 'Độ dài dữ liệu không hợp lệ.') from None
        if length < 0:
            raise ApiError(400, 'Độ dài dữ liệu không hợp lệ.')
        if length > 4096:
            raise ApiError(413, 'Nội dung gửi lên quá lớn.')
        try:
            data = json.loads(self.rfile.read(length).decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise ApiError(400, 'Dữ liệu JSON không hợp lệ.') from None
        if not isinstance(data, dict):
            raise ApiError(400, 'Dữ liệu JSON phải là một object.')
        try:
            json.dumps(data, ensure_ascii=False).encode('utf-8')
        except UnicodeEncodeError:
            raise ApiError(400, 'Nội dung có ký tự Unicode không hợp lệ.') from None
        return data

    def handle_request(self, method):
        try:
            host = self.headers.get('Host', '')
            allowed = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
            if host not in allowed:
                raise ApiError(403, 'Chỉ dùng bản thử trên localhost.')
            origin = self.headers.get('Origin')
            if method == 'POST' and origin and origin != f'http://{host}':
                raise ApiError(403, 'Nguồn yêu cầu không hợp lệ.')
            parsed = urlsplit(self.path)
            route = parsed.path
            if method == 'GET' and route in PUBLIC:
                name, media = PUBLIC[route]
                self.send(200, (ROOT / 'web' / name).read_bytes(), media)
                return
            if not route.startswith('/api/'):
                raise ApiError(404, 'Không tìm thấy đường dẫn.')
            owner = self.user()
            with closing(connect(self.server.db_path)) as db:
                if method == 'GET' and route == '/api/slots':
                    day = valid_date(parse_qs(parsed.query).get('date', [''])[0])
                    occupied = {r['slot'] for r in db.execute("SELECT slot FROM bookings WHERE date=? AND status='active'", (day,))}
                    self.send(200, {'date': day, 'slots': [{'time': t, 'available': t not in occupied and not past(day, t)} for t in SLOTS]})
                elif method == 'GET' and route == '/api/bookings':
                    rows = db.execute('SELECT * FROM bookings WHERE owner=? ORDER BY date,slot,id', (owner,)).fetchall()
                    self.send(200, {'bookings': [public_row(row) for row in rows]})
                elif method == 'POST' and route == '/api/bookings':
                    data = self.body()
                    if set(data) != {'date', 'slot', 'note'}:
                        raise ApiError(400, 'Cần đúng ngày, giờ và nội dung cuộc hẹn.')
                    day = valid_date(data['date'])
                    slot, note = data['slot'], data['note']
                    if slot not in SLOTS or not isinstance(note, str) or not 1 <= len(note.strip()) <= 80:
                        raise ApiError(400, 'Giờ hoặc nội dung cuộc hẹn chưa hợp lệ.')
                    if past(day, slot):
                        raise ApiError(400, 'Khung giờ này đã qua.')
                    key = str(uuid.uuid4())
                    try:
                        with db:
                            db.execute('INSERT INTO bookings VALUES (?,?,?,?,?,?)', (key, owner, day, slot, note.strip(), 'active'))
                    except sqlite3.IntegrityError:
                        raise ApiError(409, 'Khung giờ vừa được đặt. Hãy chọn giờ khác.') from None
                    self.send(201, {'booking': public_row(db.execute('SELECT * FROM bookings WHERE id=?', (key,)).fetchone())})
                elif method == 'POST' and re.fullmatch(r'/api/bookings/[^/]+/cancel', route):
                    if self.body():
                        raise ApiError(400, 'Yêu cầu hủy không cần thêm dữ liệu.')
                    key = route.split('/')[3]
                    with db:
                        row = db.execute('SELECT * FROM bookings WHERE id=?', (key,)).fetchone()
                        if row is None:
                            raise ApiError(404, 'Không tìm thấy lịch hẹn.')
                        if row['owner'] != owner:
                            raise ApiError(403, 'Bạn không có quyền hủy lịch này.')
                        db.execute("UPDATE bookings SET status='cancelled' WHERE id=? AND owner=?", (key, owner))
                    self.send(200, {'booking': public_row(db.execute('SELECT * FROM bookings WHERE id=?', (key,)).fetchone())})
                else:
                    raise ApiError(404, 'Không tìm thấy đường dẫn.')
        except ApiError as e:
            self.send(e.code, {'error': e.message})
        except sqlite3.Error:
            self.send(503, {'error': 'Kho dữ liệu đang bận. Hãy thử lại.'})
        except (ConnectionError, BrokenPipeError):
            pass

    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')


def create_server(db_path, port=8176):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(connect(db_path)) as db, db:
        db.execute("CREATE TABLE IF NOT EXISTS bookings (id TEXT PRIMARY KEY, owner TEXT NOT NULL, date TEXT NOT NULL, slot TEXT NOT NULL, note TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('active','cancelled')))")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS active_slot ON bookings(date,slot) WHERE status='active'")
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.db_path = db_path
    server.daemon_threads = True
    return server


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8176)
    parser.add_argument('--db', type=Path, default=ROOT/'data'/'bookings.sqlite3')
    args = parser.parse_args()
    server = create_server(args.db, args.port)
    print(f'So hen nho: http://127.0.0.1:{server.server_port} (local demo only)', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
