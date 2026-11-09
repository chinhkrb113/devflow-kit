# DevFlow Kit

**Từ yêu cầu đến phần mềm có bằng chứng kiểm tra.**

![DevFlow Kit — requirements, interactive design and verified implementation](docs/assets/hero.png)

[Bắt đầu](#cài-từ-repository) · [Kiến trúc](#kiến-trúc-bộ-kỹ-năng) · [Luồng làm việc](#luồng-làm-việc) · [Kiểm chứng](docs/verification-0.7.1.md) · [Changelog](plugin/RELEASE-NOTES.md)

DevFlow Kit kết hợp **8 thành phần kỹ năng** thành một quy trình phát triển phần mềm cùng AI: làm rõ yêu cầu, nghiên cứu hệ thống tham chiếu, viết đặc tả, dựng mock tương tác, triển khai và nghiệm thu. Agent dùng chung quyết định và tiêu chí kiểm tra qua các giai đoạn, đồng thời chỉ tải hướng dẫn phù hợp với công việc hiện tại.

Maintained by [chinhkrb113](https://github.com/chinhkrb113) · **v0.7.1** · Agent Skills / Markdown · Python installer

> A portable, reference-led workflow for coding agents. Includes design guidance, disciplined engineering and explicit verification boundaries. See the [English installation guide](plugin/INSTALL.md).

## Kiến trúc bộ kỹ năng

![Architecture: harness, devflow router, design and engineering skills, project artifacts](docs/assets/architecture.png)

`devflow` điều phối phạm vi và lựa chọn hướng dẫn; harness cung cấp mô hình, quyền truy cập tệp và công cụ thực thi. Các skill hỗ trợ quyết định và hành động của agent. Kết quả được lưu trong dự án dưới dạng tài liệu, mock, mã nguồn và bằng chứng kiểm tra.

| Nhóm | Giá trị mang lại |
|---|---|
| Yêu cầu và tham chiếu | Chuyển ý tưởng thành phạm vi rõ ràng, tìm hệ thống phù hợp và ghi nhận giả định |
| Thiết kế giao diện | Phối hợp định hướng thẩm mỹ, UX, hướng dẫn theo stack và kiểm tra giao diện thực tế |
| Xây dựng | Lập kế hoạch, debug có căn cứ, kiểm thử và review theo mức độ thay đổi |
| Nghiệm thu | Phân biệt kết quả kỹ thuật, giới hạn còn lại và quyết định chấp nhận của con người |

## Luồng làm việc

Làm rõ yêu cầu → tìm hệ thống tham chiếu → đánh giá khả thi và viết tài liệu → mock UI tương tác → phản hồi → reverse khi cần → xây dựng → kiểm tra và nghiệm thu.

![Five stages with work, constraints and outputs: understand, specify, prototype, implement, verify and accept](docs/assets/workflow.png)

Tiếp tục từ quyết định đã có. Sửa UI nhỏ giữ brand/stack và chỉ kiểm phần bị ảnh hưởng; không bắt đầu lại toàn bộ quy trình thiết kế.

Reverse là bước tùy chọn khi cần hiểu hành vi quan sát được và có quyền phân tích. Mock tương tác dùng dữ liệu mô phỏng để thống nhất trải nghiệm; kết nối backend và kiểm tra dữ liệu thật thuộc giai đoạn triển khai.

## Các thành phần

| Thành phần | Vai trò |
|---|---|
| `devflow` | Điều phối vòng đời dự án và tìm công cụ tham chiếu |
| Frontend Design | Định hướng và triển khai giao diện |
| UI/UX Pro Max | Tra cứu UX, dữ liệu thiết kế và hướng dẫn theo stack |
| Taste | Thẩm định hướng thiết kế và chất lượng giao diện |
| UI Taste by Uizze | Playbook UI web/native và bằng chứng kiểm tra |
| Ponytail | Triển khai thay đổi gọn, đủ yêu cầu |
| Caveman | Cách trả lời ngắn khi được yêu cầu |
| Superpowers | 15 profile lập kế hoạch, TDD, debug, review và xác minh |

Các thành phần dùng chung [chính sách tác vụ UI](plugin/skills/devflow/references/ui-task-policy.md) để cách gọi trực tiếp và gọi qua router nhất quán. Caveman chỉ thay đổi cách diễn đạt khi được yêu cầu; các hướng dẫn thiết kế được áp dụng theo phạm vi thay vì chạy cả bộ cho mọi chỉnh sửa.

## Cài từ repository

Yêu cầu Python 3.12+ cho installer. Sau khi clone, chọn một target và thay đường dẫn dự án:

```text
git clone https://github.com/chinhkrb113/devflow-kit.git
cd devflow-kit
python plugin/install.py --target codex --project "/path/to/project"
python plugin/install.py --target codex --project "/path/to/project" --check
```

Các target: `codex`, `claude-code`, `dsh`, `trae`, `trae-cn`; dùng `--target generic --skills-root "/exact/skills/root"` cho harness khác. Thêm `--dry-run` để xem đích; dùng `--scope user` thay cho `--project` nếu muốn cài ở cấp tài khoản.

Bộ cài tạo một bản sao đầy đủ tại `<skills-root>/devflow`. Mở phiên mới, gọi `$devflow` hoặc `/devflow` theo harness. Một số host hiển thị thêm các thành phần dưới namespace `devflow-kit:`. Không sao chép riêng một component vì các skills dùng chung policy và tài nguyên anh em.

![Portable installation: complete skill capsule, installer and supported project roots](docs/assets/portability.png)

| Harness | Target | Thư mục skill trong project | Mức kiểm chứng của bản này |
|---|---|---|---|
| Codex | `codex` | `.agents/skills` | Cài, discovery và một lượt kích hoạt mô hình chỉ đọc |
| Claude Code | `claude-code` | `.claude/skills` | Bộ cài và toàn vẹn tệp |
| DeepSeek Harness | `dsh` | `.dsh/skills` | Bộ cài và toàn vẹn tệp |
| Trae / Trae CN | `trae` / `trae-cn` | `.trae/skills` | Bộ cài và toàn vẹn tệp |
| Host khác | `generic` | Đường dẫn do người dùng chỉ định | Cần kiểm tra discovery và thực thi trên host đích |

- [Hướng dẫn cài đặt, nâng cấp và rollback](plugin/INSTALL.md)
- [Bắt đầu bằng tiếng Việt](plugin/BAT-DAU.md)
- [Khả năng hỗ trợ và giới hạn từng harness](plugin/HARNESS-COMPATIBILITY.md)
- [Mẫu đặt lịch tương tác](plugin/examples/appointment-demo/README.md)

Khi chuyển từ tên `reverse-engineered`, kiểm tra bản cũ ở cả root project/user và sao lưu ngoài discovery trước khi cài. Installer không ghi đè bản đã sửa hoặc tự gỡ bản khác.

## Bắt đầu một công việc

Sau khi host nhận skill, mô tả mục tiêu, ràng buộc và kết quả cần bàn giao. Với Codex, có thể dùng:

```text
$devflow Xây dựng công cụ quản lý công việc cho nhóm nhỏ.
Làm rõ yêu cầu, so sánh hệ thống tham chiếu, viết đặc tả và tiêu chí
nghiệm thu, rồi tạo mock tương tác để thống nhất trước khi xây dựng.
```

Với sản phẩm đã có:

```text
$devflow Sửa luồng focus của modal hiện tại. Giữ nguyên nhận diện
và stack. Kiểm tra thao tác bàn phím, đóng modal, trả focus về nút mở
và báo cáo những kiểm tra thực sự đã chạy.
```

Agent tiếp tục từ trạng thái hiện tại. Xem [hướng dẫn sử dụng](plugin/skills/devflow/references/usage.md), [quy trình hệ thống](plugin/skills/devflow/references/system-workflow.md) và [tiêu chí kiểm tra UI](plugin/skills/devflow/references/ui-acceptance.md).

## Kiểm tra và đóng gói

Full verification cần Python 3.12+, Node.js 22+, Git, Bash (Git Bash trên Windows), cùng Playwright/Chromium cho mẫu browser. Xem [README mẫu](plugin/examples/appointment-demo/README.md) để cài dependency ngoài thư mục bundle.

```text
python plugin/verify_bundle.py --with-example --report .local/verification.json
python scripts/package_skill.py --output dist/devflow-kit-v0.7.1.zip
python scripts/package_skill.py --format plugin --output dist/devflow-kit-plugin-v0.7.1.zip
```

Nếu Node/Playwright không nằm ở vị trí mặc định, dùng `--node` và `--playwright-module` hoặc biến `NODE_BINARY`, `PLAYWRIGHT_MODULE`. Packager không ghi đè ZIP có sẵn; mỗi ZIP có file SHA-256 đi kèm. Bản portable chứa `devflow/SKILL.md` cùng toàn bộ `bundle/`.

Không có shell/browser thì agent chỉ có thể áp dụng hướng dẫn; không được coi là đã chạy kiểm thử. Kết quả cài file, discovery, thực thi mô hình, kiểm tra ứng dụng và nghiệm thu con người là các bằng chứng riêng. [Báo cáo kiểm tra repository](docs/verification-0.7.1.md).

**Kết quả kiểm tra bản 0.7.1:** 118 kiểm thử đạt trên Windows; 5 adapter vượt qua kiểm tra cài lặp lại và toàn vẹn; Codex nhận 9 entry gồm entry ngoài và 8 thành phần. Đây là bằng chứng kỹ thuật cục bộ; chưa xác nhận thực thi mô hình trên mọi harness hoặc nghiệm thu production.

## Cấu trúc repository

```text
devflow-kit/
├── plugin/                 # Bộ kỹ năng phân phối
│   ├── skills/             # Router + 7 thành phần bổ trợ
│   ├── examples/           # Mẫu chạy và kiểm chứng luồng
│   ├── tests/              # Kiểm tra cấu trúc, policy, installer
│   ├── install.py          # Cài bản portable theo harness
│   └── verify_bundle.py    # Xác minh bộ kỹ năng
├── scripts/                # Đóng gói và dựng hình tài liệu
└── docs/                   # Báo cáo, nguồn diagram, SVG và PNG
```

Thay đổi tích hợp nên đi kèm cập nhật tài liệu và kiểm tra phù hợp. Khi cập nhật nguồn bên thứ ba, giữ license, ghi rõ thay đổi và cập nhật provenance/hash bằng quy trình kiểm chứng tương ứng.

## Ownership, licenses and provenance

This repository and the DevFlow Kit integration are maintained by **chinhkrb113**. Included third-party skills retain their original authorship and licenses. The repository is an adapted aggregation, not a claim that all bundled code was authored here or endorsed by its upstream authors.

- [MIT license for the original integration additions and inherited MIT code](LICENSE)
- [Component licenses, credits and modification notices](plugin/THIRD_PARTY_NOTICES.md)
- [Pinned source revisions and distributed file hashes](plugin/third-party-skills.lock.json)
- [Changelog](plugin/RELEASE-NOTES.md)

The lifecycle/catalog helper derives from [alexgaoth/awesome-reverse-engineered](https://github.com/alexgaoth/awesome-reverse-engineered). Its catalog remains an external source: use a local JSON through `RE_INDEX_DATA`, a valid cache, or network access. This repository does not include the catalog website, bulk dataset, MCP server or its refresh workflows. Project ownership metadata points here; source attribution and upstream data URLs deliberately retain their original identities.

Documentation diagrams were authored using the guidance and validation tools from [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design). Editable HTML/SVG sources, style tokens and reproduction steps are in [docs/diagrams](docs/diagrams/README.md). Diagram Design is a documentation authoring dependency, not an additional bundled runtime skill.
