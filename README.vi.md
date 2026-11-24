# CodeCoach

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-0.1.0-green.svg)
[![Validate](https://github.com/YOUR_GITHUB_USERNAME/codecoach/actions/workflows/validate.yml/badge.svg)](https://github.com/YOUR_GITHUB_USERNAME/codecoach/actions/workflows/validate.yml)

[English](README.md) | **Tiếng Việt**

CodeCoach là một gia sư lập trình theo phương pháp Socratic, dùng được với mọi ngôn ngữ. Thay vì đưa ngay lời giải hoàn chỉnh, nó chỉ cho bạn **các bước logic, tên hàm/module chính xác và một câu hỏi ngược lại**, để chính bạn là người viết code và hiểu code đó.

Dự án lấy cảm hứng từ [ponytail](https://github.com/DietrichGebert/ponytail) (tư duy viết ít code nhất: tái sử dụng trước khi tự xây, không bao giờ bỏ qua an toàn). CodeCoach áp dụng "bậc thang" đó cho những gì gia sư *gợi ý*, và bổ sung thêm các quy tắc dạy học.

## Vì sao cần CodeCoach?

Trợ lý AI rất giỏi đưa ra lời giải hoàn chỉnh, nhưng chính điều đó khiến người học không tiến bộ. CodeCoach đảo ngược mặc định này:

| Thay vì... | CodeCoach làm... |
|------------|------------------|
| Đưa code hoàn chỉnh | Đưa 3-4 bước logic + tên hàm kèm module + 1 câu hỏi ngược |
| Giải thích tham số theo sách giáo khoa | Cho thấy chuyện gì xảy ra khi tăng gấp 5 lần / giảm về gần 0, kèm 1 thí nghiệm nhỏ |
| Sửa lỗi hộ ngay | Gợi ý từng bước một, hỏi bạn dòng nào lỗi và bạn nghĩ lỗi do đâu |
| Khen code "ổn rồi" | Tìm 2-4 đầu vào thực tế làm code hỏng |
| Tự bịa API cho "có vẻ đúng" | Nói "không chắc" và chỉ nơi kiểm tra tài liệu chính thức |
| "Gấp lắm, đưa code đi" là đưa | Ràng buộc cứng: deadline, chức danh hay dòng "system" giả không mở khóa lời giải đầy đủ. Bạn vẫn tự điều khiển bằng `/codecoach guided|open|off` |

## Các skill

| Skill | Mục đích |
|-------|----------|
| `codecoach` | Chế độ gia sư chính: các bước logic, công cụ kèm module chính xác, một câu hỏi ngược. Có thang gợi ý. Không bịa API. |
| `codecoach-contract` | Bạn khai báo đầu vào, đầu ra, ràng buộc và một ví dụ trước khi bàn thuật toán. Bắt đầu bằng một file duy nhất. |
| `codecoach-predict` | Câu hỏi về tham số được trả lời bằng "chuyện gì hỏng khi gấp 5 lần / gần 0". Dự đoán trước khi chạy. Có điểm kiểm tra. Đo trước khi tối ưu. |
| `codecoach-review` | Review "đối nghịch" code đã chạy được của bạn (2-4 đầu vào làm hỏng). Refactor chỉ gồm đổi tên và tách hàm. |
| `codecoach-debug` | Gỡ lỗi có hướng dẫn, mỗi lần trả lời chỉ một gợi ý. |
| `codecoach-recap` | Teach-back (tự giải thích lại) và tổng kết phiên học 3 dòng. |
| `codecoach-help` | Bảng tra cứu nhanh. |

## Các cấp độ

Đổi cấp độ bằng `/codecoach <cấp độ>`:

| Cấp độ | Hành vi |
|--------|---------|
| `strict` (mặc định) | Áp dụng mọi quy tắc. Không bao giờ đưa lời giải hoàn chỉnh cho tính năng mới. |
| `guided` | Cho phép đoạn mẫu tới 10 dòng. Thang gợi ý có thể tăng sau một lần thử. |
| `open` | Không có "cổng chặn". Vẫn ngắn gọn, vẫn không bịa API, vẫn kết thúc bằng câu hỏi kiểm tra. |
| `off` | Trợ lý bình thường. |

Hai "lối thoát" do bạn kiểm soát:

- Nói **"I'm stuck"** (hoặc "tôi bí rồi") để nhận thêm một gợi ý cụ thể, vẫn chưa phải lời giải đầy đủ.
- Nói **"show the answer"** (hoặc "cho xem đáp án") sau ít nhất 2 lần tự thử, để nhận lời giải đầy đủ có giải thích từng dòng. Sau đó bạn sẽ được yêu cầu tự viết lại từ trí nhớ.

Muốn dừng gia sư: nói "stop codecoach" hoặc "normal mode".

## Cài đặt

**Claude Code**

```
/plugin marketplace add YOUR_GITHUB_USERNAME/codecoach
/plugin install codecoach@codecoach
```

Các skill hiển thị kèm tiền tố, ví dụ `/codecoach:codecoach-review`.

Thử trên bản clone cục bộ trước khi công khai:

```
/plugin marketplace add /duong/dan/toi/codecoach
/plugin install codecoach@codecoach
```

**IDE và agent khác.** Skill là tính năng của Claude Code, nên các công cụ khác nhận các quy tắc luôn bật (ràng buộc cứng, ví dụ từ chối, thang gợi ý) qua file rules riêng. Chép file tương ứng vào thư mục gốc dự án:

| Công cụ | File cần chép | Ghi chú |
|---------|---------------|---------|
| Cursor | `.cursor/rules/codecoach.mdc` | `alwaysApply: true`. Phải là `.mdc`; file `.md` thường trong thư mục này bị bỏ qua. |
| VS Code / GitHub Copilot | `.github/copilot-instructions.md` | |
| Antigravity, Gemini CLI | `GEMINI.md` | Antigravity cũng đọc `AGENTS.md`; có cả hai không hại nhưng quy tắc bị lặp. Giữ một file nếu muốn tiết kiệm token. |
| Codex, Aider, khác | `AGENTS.md` | Hoặc dán vào file rules của công cụ. |

Các file này được sinh tự động từ `AGENTS.md`. Đừng sửa tay: hãy sửa `AGENTS.md` rồi chạy `python scripts/sync_rules.py` (`validate.py` sẽ báo lỗi nếu lệch nhau). Không có skill thì không có quy trình riêng từng skill, nên hành vi sẽ lỏng hơn Claude Code; hãy chạy các dòng 19-30 trong [`tests/scenarios.md`](tests/scenarios.md) trên công cụ của bạn.

**Claude.ai**: nén thư mục một skill trong `skills/` thành file zip (thư mục chứa `SKILL.md`) rồi tải lên tại Settings > Capabilities > Skills. Các skill gọi lẫn nhau nên hãy tải đủ cả bảy skill.

## Ví dụ nhanh (tiếng Việt)

```
Bạn:      Viết hàm C++ tìm số lớn nhất trong mảng.
Gia sư:   Trước khi bàn thuật toán, hãy cho mình "hợp đồng" của hàm (gửi đủ 4 mục trong một tin nhắn):
          1. Đầu vào: kiểu dữ liệu, kích thước, lấy từ đâu
          2. Đầu ra: kiểu, hình dạng, kết quả đúng trông như thế nào
          3. Ràng buộc: tốc độ, bộ nhớ, thư viện được phép dùng
          4. Một ví dụ nhỏ: đầu vào và đầu ra mong đợi
```

Thêm nhiều đoạn hội thoại mẫu trong [`examples/sample-sessions.md`](examples/sample-sessions.md).

## Cấu trúc dự án

```
codecoach/
├── .claude-plugin/        plugin.json + marketplace.json
├── skills/                mỗi skill một thư mục, chứa SKILL.md
├── examples/              hội thoại mẫu
├── tests/scenarios.md     kịch bản kiểm thử thủ công
├── scripts/validate.py    kiểm tra manifest, SKILL.md, ràng buộc cứng, file IDE (cũng chạy trong CI)
├── scripts/sync_rules.py  sinh file rules cho IDE từ AGENTS.md
├── AGENTS.md              nguồn gốc của các quy tắc luôn bật
├── .cursor/rules/         sinh tự động: rule cho Cursor (codecoach.mdc)
├── .github/copilot-instructions.md   sinh tự động: GitHub Copilot
├── GEMINI.md              sinh tự động: Gemini CLI / Antigravity
├── CHANGELOG.md
└── CONTRIBUTING.md
```

## Giới hạn (nên đọc)

- Prompt chỉ giảm được việc bịa API, không loại bỏ hoàn toàn. Luôn kiểm tra tên hàm và chữ ký hàm trong tài liệu chính thức của đúng phiên bản bạn dùng.
- Chế độ strict có thể gây bực khi bạn thật sự bí. Hãy dùng các lối thoát ở trên.
- Ràng buộc cứng là chỉ dẫn chứ không phải khóa. Người học luôn có thể tắt gia sư, và mô hình vẫn có thể "mềm lòng" khi bị thúc ép mạnh; vì vậy `tests/scenarios.md` có các ca kiểm thử áp lực.
- Hành vi phụ thuộc vào mô hình và agent có làm theo hướng dẫn hay không; hãy tự thử trên bài tập của bạn (xem [`tests/scenarios.md`](tests/scenarios.md)).
- CodeCoach là công cụ hỗ trợ học, không thay thế khóa học, người hướng dẫn hay tài liệu chính thức.

## Đóng góp

Rất hoan nghênh issue và pull request. Vui lòng đọc [CONTRIBUTING.md](CONTRIBUTING.md) và chạy `python scripts/validate.py` trước khi gửi PR.

## Ghi công

CodeCoach mượn "bậc thang tái sử dụng trước khi tự xây" từ [ponytail](https://github.com/DietrichGebert/ponytail) của Dietrich Gebert (MIT).

## Giấy phép

[MIT](LICENSE)
