# DevFlow Kit — AI Development Skills — 0.8.0

Bản portable có một điểm vào `devflow`, chứa đủ chín thành phần. Giữ nguyên toàn bộ thư mục này; đừng chỉ lấy SKILL.md. Bản cài là bản sao độc lập, không phụ thuộc junction, symlink hoặc thư mục tải về.

## Cài bằng Python trên Windows/macOS/Linux

Mở terminal tại thư mục `devflow` vừa giải nén. Dùng Python 3.12+ (`python`, `python3` hoặc `py -3` tùy máy). Chọn **một** lệnh theo harness và thay đường dẫn dự án bằng đường dẫn có thật:

```text
python bundle/install.py --target codex --project "/path/to/project"
python bundle/install.py --target claude-code --project "/path/to/project"
python bundle/install.py --target dsh --project "/path/to/project"
python bundle/install.py --target trae --project "/path/to/project"
```

Trên Windows có thể dùng `--project "D:\My Project"`; trên macOS/Linux dùng đường dẫn tương ứng. Với Trae CN chọn `--target trae-cn`. Muốn cài cho tài khoản hiện tại thay `--project ...` bằng `--scope user`. DSH ở đây là DeepSeek Harness, cần filesystem skill provider được bật trong cấu hình harness.

Thêm `--dry-run` để xem đích mà chưa ghi; thêm `--check` để kiểm nội dung bản đã cài. Cài lại cùng bản bỏ qua; xung đột hoặc file đã thay đổi sẽ dừng, không ghi đè. Nếu bị gián đoạn do hết đĩa/quyền, thư mục mới có thể chưa đủ; kiểm tra báo lỗi trước khi dùng. Bộ cài không tự xóa hay sửa một bản đang có.

Bản 0.8.0 kiểm cả file thừa và link trong bản cài, kể cả `SKILL.md`/script giấu trong thư mục cache hoặc evidence; lỗi trả mã 2 và không xóa file. Chỉ miễn trừ báo cáo mặc định, ảnh/log/JSON/video evidence phẳng của mẫu và cache Python `.pyc` dưới `__pycache__`. Đặt dependency, bản thử và báo cáo tùy chỉnh ngoài thư mục skill. Khi nâng cấp, dùng bộ cài mới để kiểm, giữ bản cũ ở nơi riêng ngoài thư mục discovery rồi cài vào đích trống; không trộn phiên bản. Xem [quy tắc kiểm bản cài](bundle/INSTALL.md).

Ngoài ra cho phép đúng năm output của test UI trong `evidence/ui-redesign/`: `ui-states.json` và `mock-320.png`, `mock-390.png`, `mock-768.png`, `mock-1440.png`; không miễn trừ cả cây thư mục. Verifier kiểm lại tính toàn vẹn sau khi chạy test.

Harness khác: tra thư mục skills của nó rồi dùng:

```text
python bundle/install.py --target generic --skills-root "/exact/skills/root"
```

Lệnh thêm thư mục con `devflow`; không nhập đường dẫn SKILL.md làm skills root. Không tự thêm vào tất cả harness hoặc sửa AGENTS.md/CLAUDE.md/cấu hình tài khoản.

## Cài thủ công, không chạy bộ cài

Sao chép **toàn bộ thư mục `devflow`** vào một trong các skills root sau; tên thư mục `devflow` khớp tên skill:

| Harness | Trong dự án | Cấp người dùng |
|---|---|---|
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| DeepSeek Harness | `.dsh/skills/` | `~/.dsh/skills/` |
| Trae | `.trae/skills/` | `~/.trae/skills/` |
| Trae CN | `.trae/skills/` | `~/.trae-cn/skills/` |

Nếu đã có cùng tên, giữ bản cũ ở nơi riêng đã kiểm tra trước khi cài bản mới; không trộn hai phiên bản. Đích phải có `devflow/SKILL.md` cùng `devflow/bundle/`. Với config home tùy chỉnh, dùng thư mục thực của harness. Installer tôn trọng `CLAUDE_CONFIG_DIR` và `DSH_HOME` khi cài user scope.

## Gọi và kiểm tra thật

Mở phiên mới hoặc refresh danh sách skill, xác nhận đúng tên và đường dẫn. Codex thường gọi `$devflow`; Claude Code và DSH gọi `/devflow`; Trae dùng skill selector hoặc yêu cầu agent dùng `devflow`. Tên thực trong UI là căn cứ cuối cùng; chính sách quản trị/phiên bản harness có thể chặn skill.

Prompt thử chỉ đọc:

```text
Dùng devflow từ bản cài trong project này. Đọc router và hướng dẫn UI.
Giải thích luồng xây ứng dụng đặt lịch, vai trò bốn skill giao diện, Ponytail và Caveman.
Giữ brand/mock đã duyệt. Không có Uizze MCP và native runner thì phần nào chưa kiểm chứng?
Chỉ đọc; ghi lại những đường dẫn thực sự đã đọc. Không sửa app hoặc bật chế độ trả lời.
```

Kiểm tra tool trace có đọc đúng file và references; câu trả lời tự nhận “đã dùng skill” không đủ. Một điểm vào portable không làm mất chín thành phần: agent đọc từng phần theo công việc. [Ma trận tương thích](bundle/HARNESS-COMPATIBILITY.md) phân biệt cài đúng định dạng, discovery và chạy mô hình.

Sửa UI nhỏ qua router hoặc gọi trực tiếp đều dùng [chính sách UI chung](bundle/skills/devflow/references/ui-task-policy.md): giữ brand/stack, chỉ đọc phần liên quan, sửa và kiểm tra hành vi bị ảnh hưởng. Không tự sinh design system, vẽ hướng mới hay đọc toàn bộ playbook app chỉ để sửa một control. Khi làm mới hoặc redesign đã được yêu cầu, mới dùng luồng đầy đủ.

Một số host còn quét các SKILL.md bên trong: Bản 0.5.1 từng được kiểm trên Codex 0.159.2 với điểm vào ngoài và bảy thành phần. Bản 0.6.0 đã bổ sung Superpowers thành tám thành phần; 0.7.0 đổi tên thành DevFlow Kit; xem báo cáo phát hành cho discovery thực tế. Đây không phải yêu cầu cho host khác; luôn có thể gọi điểm vào `devflow` rồi để nó đọc thành phần. Khi có nhiều bản cài, chọn đúng đường dẫn project thay vì chỉ dựa vào tên.

## AI chat hoặc nền tảng tải ZIP

Nếu nền tảng nhận Agent Skill ZIP, thử ZIP portable gốc chứa thư mục `devflow/SKILL.md`; không upload ZIP legacy có gốc `plugin/`. Tính năng/giới hạn file phụ thuộc tài khoản và host, cần kiểm tra sau import. Không tự đồng nhất Claude Code local với Claude.ai/Cowork/cloud.

AI có thể đọc tệp nhưng không có cơ chế skills: mở [SKILL.md](SKILL.md), yêu cầu dùng nó và đọc các reference được dẫn. AI chỉ nhận văn bản: dán SKILL.md và phần reference cần thiết theo từng bước. Đây là sử dụng hướng dẫn theo phiên, không phải cài skill tự động hay bằng chứng đã chạy helper/browser. Không có filesystem, shell hoặc browser thì không thể hứa thực thi toàn bộ luồng; agent phải ghi phần còn pending.

## Kiểm tra gói và mẫu

```text
python bundle/verify_bundle.py
python bundle/verify_bundle.py --with-example
```

Full verification cần Python 3.12+, Node 22+, Git; mẫu browser còn cần Playwright/Chromium theo [README mẫu](bundle/examples/appointment-demo/README.md). Đọc Markdown/cài thủ công không cần các runtime này. `verify_bundle.py` kiểm file trong bundle; checksum ZIP đi kèm kiểm toàn bộ bản tải về. Installer kiểm nội dung nguồn trước khi copy; thiếu dependency/skipped checks không được tính là full pass.

[Hướng dẫn mẫu](bundle/BAT-DAU.md) · [Giấy phép](bundle/THIRD_PARTY_NOTICES.md) · [Luồng UI](bundle/skills/devflow/references/ui-workflow.md)

## Dùng Superpowers

Bản này bổ sung Superpowers upstream 7.0.2 với 15 quy trình trong một điểm vào. Ví dụ: “Dùng devflow và Superpowers systematic-debugging để sửa lỗi validation, giữ brand/stack; yêu cầu đã duyệt, không làm lại discovery.” Hoặc gọi trực tiếp tên `superpowers` do harness hiển thị. Agent đọc [điểm vào](bundle/skills/superpowers/SKILL.md), policy và đúng profile cần dùng.

Các file profile tên GUIDE.md để tránh tự kích hoạt thêm 15 entry. Không có hook SessionStart hay cấu hình global được đăng ký. Không có subagent thì chạy tuần tự và ghi rõ self-review; không có shell/browser thì các kiểm chứng tương ứng còn pending. Quy trình đầy đủ không áp đặt lên sửa UI nhỏ. Helper kế hoạch cần Bash/Git/POSIX; suite test đầy đủ cần Bash hoạt động, có thể đặt `BASH_BINARY`. Visual companion là tùy chọn, không thay mock sản phẩm; tải ảnh telemetry từ xa đã tắt trong bản này.

## Chuyển từ tên cũ

Kiểm tra bản project và user có `reverse-engineered`, `find-reverse-engineered` hoặc `reverse-engineered-*`. Sao lưu đúng bản cũ ra ngoài thư mục discovery; với junction chỉ gỡ liên kết đã xác minh, giữ thư mục đích. Cài bản mới vào `skills/devflow`, chạy `--check`, rồi mở phiên mới. Bộ cài dừng nếu còn tên cũ trong skills root đã chọn; không tự xóa hay ghi đè. Xem [nâng cấp và quay lại bản cũ](bundle/INSTALL.md#upgrade-from-reverse-engineered-06x-and-earlier).

Bản 0.8.0 bổ sung Diagram Design thành chín thành phần. Gọi `devflow` để vẽ kiến trúc/luồng; hướng dẫn [Diagram Design](bundle/skills/diagram-design/SKILL.md) dùng tài nguyên nội bộ, giữ style và đầu ra trong dự án.
