# DevFlow Kit — AI Development Skills — 0.8.0

**Bản đa harness:** nếu ZIP có gốc `devflow/`, bắt đầu từ `START-HERE.md` ở thư mục ngoài. Bộ cài mới là `python bundle/install.py --target codex|claude-code|dsh|trae --project <thư-mục-dự-án>` (chọn một target). Nội dung dưới đây dành cho bản legacy `plugin/` hoặc đọc từ `bundle/` để chạy mẫu. [Ma trận tương thích](HARNESS-COMPATIBILITY.md) ghi rõ phạm vi hỗ trợ.

Giải nén toàn bộ ZIP vào một thư mục cố định, rồi mở terminal tại thư mục `plugin` chứa file này. Không tách riêng các SKILL.md: script, dữ liệu, tài nguyên và các skill anh em phải ở cùng gói.

## 1. Cài vào Codex

Trên Windows PowerShell, từ thư mục `plugin` vừa giải nén:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-codex.ps1
```

Lệnh tạo junction trong `~/.agents/skills`, không sửa bản skill cá nhân khác. Chạy lại cùng nguồn sẽ bỏ qua các link đã đúng. Nếu trùng tên từ nguồn khác, trình cài dừng: xem [cách cập nhật/gỡ](INSTALL.md) trước khi đổi link. Giữ nguyên thư mục giải nén vì các link phụ thuộc vào nó. `ExecutionPolicy Bypass` ở đây chỉ áp dụng cho tiến trình chạy lệnh, không đổi chính sách máy.

Mở lượt hoặc phiên Codex mới. Ví dụ yêu cầu:

```text
$devflow-kit:devflow
Tôi muốn xây một ứng dụng đặt lịch mẫu. Hãy làm rõ phạm vi, tìm tham chiếu,
viết đặc tả, làm mock tương tác bằng cả bốn skill UI trong bộ, reverse khi
thật sự cần, rồi xây và kiểm thử local. Tôi giao bạn chọn các chi tiết của
mẫu thử; ghi rõ giả định, kết quả kiểm tra và phần chưa kiểm chứng.
```

Tên có thể khác tùy host; kiểm tra tên/path trong danh sách skill. Nếu chưa thấy, mở phiên mới hoặc làm mới client. Không suy ra đã kích hoạt chỉ từ việc cài file. [Hướng dẫn discovery/activation](skills/devflow/references/codex.md) phân biệt từng bước.

## 2. Tám thành phần trong gói

Trong bản 0.8.0, gọi trực tiếp từng skill UI hay qua router đều áp dụng [chính sách UI chung](skills/devflow/references/ui-task-policy.md). Sửa component nhỏ giữ brand/stack, chỉ đọc hướng dẫn liên quan và kiểm hành vi cần sửa; không chạy lại cả quy trình thiết kế. Taste có điểm vào ngắn, giữ playbook đầy đủ trong reference để đọc khi cần.

| Skill | Vai trò |
|---|---|
| devflow | Điều phối yêu cầu → tham chiếu → đặc tả → mock → reverse nếu cần → xây → nghiệm thu |
| ui-ux-pro-max | Tra cứu UX, accessibility, responsive, trạng thái và stack |
| frontend-design | Chọn một hướng thiết kế, bố cục, typography và triển khai |
| design-taste-frontend | App/site mode, hỗ trợ hướng thiết kế, lint và kiểm tra thị giác bằng trình duyệt |
| ui-taste (Uizze) | Playbook web/iOS, ảnh mục tiêu khi phù hợp, kiểm tra bằng chứng thị giác |
| ponytail | Triển khai gọn nhưng đủ phạm vi, giữ validation và kiểm thử cần thiết |
| superpowers | 15 quy trình: làm rõ, lập kế hoạch, TDD, debug, review, worktree, kiểm chứng và chẩn đoán phiên khi được yêu cầu |
| caveman | Trả lời ngắn khi được yêu cầu; giữ nguyên ý nghĩa, số liệu và ngôn ngữ |

Yêu cầu và brand/stack đã có được ưu tiên. Xem [luồng UI](skills/devflow/references/ui-workflow.md) và [checklist tương tác](skills/devflow/references/ui-acceptance.md). Mock, backend thật, nghiệm thu con người và phát hành là các bằng chứng/quyết định riêng.

## 3. Tự kiểm tra và mở dự án mẫu

Ví dụ dùng bổ sung: “Áp dụng Ponytail để triển khai đủ đặc tả với thay đổi gọn”; “Dùng UI Taste của Uizze kiểm tra mock theo hướng thiết kế đã duyệt”; “Dùng Caveman trả lời ngắn bằng tiếng Việt”. Cài gói không tự bật chế độ trả lời. Chỉ có core Ponytail/Caveman; ultra/wenyan của Caveman không nằm trong bản này. UI Taste chạy local không cần tài khoản/MCP trả phí. Xem [quy tắc phối hợp](skills/devflow/references/coding-communication.md).

Môi trường đã kiểm chứng: Windows, Python 3.12, Node.js 24, Codex 0.159.2. Bộ kiểm tra yêu cầu Python 3.12+, Node.js 22+ và Git; không tự cài dependency. Có thể dùng `python3` hoặc `py -3` thay `python` nếu đó là interpreter đã cài.

```powershell
python verify_bundle.py
```

Lệnh kiểm hash bản phát hành, tài nguyên/link, các helper UI và regression catalog. Thiếu dependency hoặc skipped test không được báo full pass. Kết quả ở `verification-report.json`; xem trường `not_executed` để biết phạm vi chưa chạy.

Chạy thử UI không cần Node/Playwright, chỉ cần Python:

```powershell
cd examples/appointment-demo
python server.py --port 8176 --db "$env:USERPROFILE/Documents/appointment-demo/bookings.sqlite3"
```

Mở [mock](http://127.0.0.1:8176/?mock=1) hoặc [API/SQLite thật](http://127.0.0.1:8176/). DB ở ngoài thư mục skill để lần kiểm bản cài sau vẫn hợp lệ. Nếu port bận, chọn một port khác bằng `--port` và sửa URL tương ứng. Dừng server bằng Ctrl+C. Mẫu chỉ có dữ liệu giả An/Bình, không có đăng nhập production.

Để chạy kiểm thử browser/backend/restore tự động, theo [README mẫu](examples/appointment-demo/README.md), rồi từ thư mục `plugin`:

```powershell
python verify_bundle.py --with-example --playwright-module "C:/path/to/external/node_modules/playwright"
```

## 4. Nội dung và giới hạn

Gói có source mẫu sạch, không kèm DB, cache, profile trình duyệt hay báo cáo chứa đường dẫn máy tác giả. Báo cáo mới được sinh trên máy người chạy. Catalog 17.000+ dự án được tải khi cần, hoặc dùng cache/dataset do người dùng cung cấp; ZIP không chứa toàn bộ catalog. Tra cứu UX và thư viện Taste đã nằm trong gói.

Thay đường dẫn Playwright mẫu bằng vị trí đã cài ngoài thư mục skill. Xem [thay đổi 0.8.0](RELEASE-NOTES.md), [giấy phép thành phần](THIRD_PARTY_NOTICES.md) và `RELEASE-MANIFEST.json` trong ZIP. Bản chạy local không phải chứng nhận production hoặc thử nghiệm của người dùng mới. macOS/Linux có hướng dẫn link trong INSTALL.md nhưng chưa được chạy thực tế trong lượt phát hành này.

Superpowers được đóng gói theo [policy tích hợp](skills/superpowers/references/compatibility.md), đọc từng profile khi cần. Dùng chung với Ponytail và bốn skill UI trong cùng phạm vi; không chạy lại discovery/approval đã xong. Helper kế hoạch cần Bash/Git, companion cần Node và renderer cần Graphviz khi dùng; các công cụ đó không bắt buộc để đọc hướng dẫn.

## Vẽ kiến trúc và luồng

Bản 0.8.0 có chín thành phần, bao gồm [Diagram Design](skills/diagram-design/SKILL.md). Yêu cầu `devflow` đọc hệ thống hiện tại, phân biệt phần đã có/phần đề xuất và vẽ kiến trúc. Giữ HTML/SVG để chỉnh sửa, chạy kiểm tra cấu trúc/hình học và xem ảnh render; PNG cần browser phù hợp. Không sửa style trực tiếp trong bản cài.
