# Sổ hẹn nhỏ — mẫu sạch để chạy thử skill

Mẫu dùng HTML/CSS/JS, Python stdlib và SQLite; không cần cài package Python. Python 3.12+ là môi trường hỗ trợ của bản đóng gói này.

```text
python server.py --port 8176 --db "/absolute/private-workspace/appointment-demo/bookings.sqlite3"
```

Thay đường dẫn DB bằng vị trí ngoài thư mục bản cài, ví dụ `C:/Users/your-name/Documents/appointment-demo/bookings.sqlite3` trên Windows. Mở http://127.0.0.1:8176/?mock=1 để dùng localStorage giả lập, hoặc http://127.0.0.1:8176/ để dùng HTTP/SQLite. Chỉ bind loopback. Nếu bỏ `--db`, server tạo `data/bookings.sqlite3` bên cạnh source; chỉ dùng mặc định này khi đã sao chép mẫu ra workspace riêng. Dừng bằng Ctrl+C. Không xóa DB để khắc phục lỗi giao diện.

## Thử bằng tay

1. Chọn An; chọn ngày tương lai bằng dải ngày hoặc input, chọn giờ trống.
2. Để nội dung trống và bấm xác nhận: lỗi xuất hiện, focus về field. Nhập nội dung mẫu: lỗi tương ứng biến mất.
3. Xác nhận; lịch xuất hiện trong Lịch của tôi. Tải lại trang rồi mở danh sách: dữ liệu còn.
4. Đổi Bình: không thấy chi tiết lịch của An; giờ An đặt không chọn được.
5. Đổi lại An và hủy: trạng thái Đã hủy, giờ mở lại.
6. Thử bàn phím Enter/Tab ở dải ngày; focus không mất sau cập nhật. Thử desktop/tablet/mobile; dải ngày có scroll riêng ở 320px, trang không tràn ngang.
7. Trong mock, **Xóa dữ liệu mock** chỉ xóa dữ liệu giả của trình duyệt; nút bị khóa khi gửi. Đổi danh tính xóa ghi chú đang nhập. Dữ liệu demo không phải bảo mật production.

## Chạy kiểm tra tự động

Backend:

```text
python -m unittest -v test_server
```

Toàn luồng cần Node.js 22+ và Playwright/Chromium. `package.json` pin phiên bản Playwright đã được dùng khi phát hành. Nếu chưa có Playwright, sao chép toàn bộ thư mục `appointment-demo` ra workspace riêng ngoài bản cài, mở terminal tại bản sao đó rồi chạy:

```text
npm install
npx playwright install chromium
python verify.py
```

Việc cài dependency/browser cần mạng và chỉ phục vụ test. Có thể dùng một Playwright đã cài ở nơi khác bằng `python verify.py --node <node-executable> --playwright-module <absolute-playwright-directory>`. Không nhập nguyên dấu `<...>`; thay bằng đường dẫn thật. Runtime app không dùng Node/Playwright.

Trong bản ZIP/bản cài 0.5.1, dùng Playwright ở thư mục dependency bên ngoài hoặc sao chép mẫu ra workspace riêng trước khi `npm install`. `node_modules`/lockfile tạo trong bản cài sẽ bị kiểm kê báo file thừa; không miễn trừ cả thư mục có thể chứa script/skill. Evidence JSON/log/PNG/video phẳng trong `evidence/` và cache Python được cho phép, nhưng không phải bằng chứng có sẵn của bản phát hành.

Bộ kiểm tra cũng cho phép đúng `evidence/ui-redesign/ui-states.json` và bốn ảnh `mock-320.png`, `mock-390.png`, `mock-768.png`, `mock-1440.png` do test trạng thái UI tạo. File lạ khác trong thư mục con này vẫn bị từ chối.

`verify.py` tạo DB, port và browser context tạm; kiểm mock không ghi DB thật, browser → API → SQLite, quyền, conflict, phản hồi đến muộn, reload/restart và backup/restore. Không chạy hai verifier đồng thời vào cùng `evidence/`. Lệnh ghi kết quả và hash source vào `evidence/acceptance.json` rồi trả nonzero khi có lỗi. `test_ui_states.cjs` được gọi trong runner; không cần chạy thủ công trên DB đang dùng.

Từ thư mục gốc `plugin` (hoặc `bundle` trong bản portable), dùng `python verify_bundle.py --with-example --playwright-module "/absolute/private-workspace/appointment-demo/node_modules/playwright"` để kiểm cả bundle và mẫu bằng dependency bên ngoài; thay đường dẫn bằng vị trí đã cài thực tế. Danh sách báo cáo đọc cùng `result`, không suy ra thành công từ việc file tồn tại.

## Phạm vi

Hai danh tính demo công khai An/Bình, một người tư vấn, sáu khung 30 phút, UTC+07. Contract ở api-contract.json. Không thanh toán, email/SMS, OAuth, hosting hay tài khoản thật. Reverse không cần vì hợp đồng được định nghĩa rõ và không có giao thức/binary cần giải mã.

Các fixture đặt lịch dùng ngày 2030-11-04/05; khi chạy sau thời điểm đó cần cập nhật fixture hoặc dùng đồng hồ test cố định, không bỏ kiểm tra ngày quá khứ. Nghiệm thu local không thay human acceptance, đánh giá screen reader hay release production.
