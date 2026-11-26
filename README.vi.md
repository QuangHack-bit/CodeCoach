# CodeCoach Custom (v2)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-0.2.0-green.svg)
[![Validate](https://github.com/QuangHack-bit/CodeCoach/actions/workflows/validate.yml/badge.svg)](https://github.com/QuangHack-bit/CodeCoach/actions/workflows/validate.yml)

[English](README.md) | **Tiếng Việt**

**CodeCoach Custom v2** là hệ thống huấn luyện tư duy lập trình đóng vai **Đàn anh Senior nghiêm khắc** theo phương pháp Socratic: không nịnh, không viết hộ logic lõi, ép thiết kế **`.md` trước – Code sau**, giải phẫu khung biến & ma trận tham số, và **Debug 3 cổng bằng chứng kèm trích nguồn bắt buộc (`H4+`)**.

Tối ưu chuyên sâu cho 3 mảng: **Nhúng & Vi điều khiển (`C/C++`, MCU/STM32)**, **AI & Robotics (`Python`, Thị giác máy tính, `ROS 2`)**, và **Nền tảng Phần mềm (`Java`, OOP, DSA)** — kế thừa kỷ luật tối giản và khóa phạm vi từ [ponytail](https://github.com/DietrichGebert/ponytail).

## Điểm nâng cấp cốt lõi ở bản v2

1. **Luật `.md` Trước – Code Sau (`codecoach-blueprint`):** Thay thế `codecoach-contract`. Khóa tạo mã nguồn cho đến khi chốt xong file thiết kế (`ARCHITECTURE.md` hoặc `docs/DESIGN_<feature>.md`) gồm: Hợp đồng dữ liệu/phần cứng, Sơ đồ luồng ASCII/Mermaid, Bản đồ hàm trọng yếu, và Biến trạng thái & Edge cases.
2. **Giải phẫu Khung Code 3 Lớp (`codecoach-anatomy`):** Trình bày **Bảng biến bắt buộc**, **Ví dụ cơ chế cô lập/tương tự**, và **Ma trận chọn tham số** (`Thấp / Tiêu chuẩn / Cao`) thay vì giấu cộc lốc hay làm hộ bài toán chính.
3. **Chuỗi Giải thích Bản chất 3 Bước:** `Ví dụ đời thực (Analogy 2-3 câu)` -> `Sơ đồ ASCII/Mermaid` -> `Nguyên lý gốc (CPU, bộ nhớ, phần cứng, toán học) & đánh đổi`.
4. **Debug 3 Cổng Bằng Chứng & Luật Trích Nguồn `H4+` (`codecoach-debug`):** Cấm đoán mò/sửa mò. Bắt buộc qua: Cổng 1 (Thu thập log/code/môi trường) -> Cổng 2 (Thực nghiệm khoanh vùng có kết quả thật) -> Cổng 3 (Hướng sửa nguyên nhân gốc). Mọi thông tin ngoài workspace phải trích rõ `[Nguồn: <Tài liệu + Phiên bản> — Vị trí: <Mục/Trang/Hàm>]` hoặc gắn nhãn **`[CHƯA KIỂM CHỨNG]`** (`[UNVERIFIED]`).
5. **Gói Luật Chuyên biệt Theo Mảng (`codecoach-domains`):** Pack A (`*.java`, DSA: bất biến vòng lặp, $O(\cdot)$, OOP, test biên) & Pack B (`*.c/*.cpp/*.h/*.py`: `SPI/I2C/UART/DMA`, ngắt `ISR`, bộ nhớ tĩnh/buffer, CV & `ROS 2`).
6. **Hồ sơ Học tập Xuyên phiên (`.codecoach/learner-profile.md`):** Tự động đọc đầu phiên để bỏ qua lý thuyết `Mastered` và cảnh báo sớm `Recurring Blind Spots`.
7. **Biên dịch Rule Đa Nền tảng (`scripts/sync_rules.py`):** Sinh tự động bộ `.cursor/rules/*.mdc` theo glob, `.github/instructions/*.instructions.md` cho Copilot, và `GEMINI.md` chống nạp trùng token với `AGENTS.md` trên Antigravity / Gemini CLI.

## Danh sách 9 Skills (v2)

| Skill | Chức năng |
| :--- | :--- |
| `codecoach` | Lõi điều phối Senior Socratic: cấm nịnh, khóa phạm vi Ponytail, giải thích 3 bước, thang gợi ý 4 tầng, luật cứng `H1`–`H6` & `H4+`. |
| `codecoach-blueprint` | Cổng kiến trúc `.md` trước khi code (`ARCHITECTURE.md` / `docs/DESIGN_<feature>.md`): Hợp đồng, Sơ đồ luồng, Hàm trọng yếu, Biến & Biên. |
| `codecoach-anatomy` | Giải phẫu khung code 3 lớp: Bảng biến bắt buộc + Đoạn mẫu cơ chế cô lập + Ma trận chọn tham số (Thấp / Chuẩn / Cao). |
| `codecoach-debug` | Debug 3 cổng bằng chứng (Khóa bằng chứng -> Kiểm chứng thực nghiệm -> Hướng fix gốc) + trích nguồn `H4+` hoặc `[CHƯA KIỂM CHỨNG]`. |
| `codecoach-domains` | Gói luật chuyên ngành: **Pack A** (Java/OOP/DSA) và **Pack B** (Nhúng C/C++, MCU/STM32, ISR/DMA, CV & ROS 2). |
| `codecoach-predict` | Phân tích độ nhạy tham số (`Low / Nominal / High` & `5x / gần 0`), dự đoán trước khi chạy, đặt 1 checkpoint, đo đạc trước khi tối ưu. |
| `codecoach-review` | Review PR gắt kiểu Senior trên code đã chạy (chỉ ra 2–4 kịch bản làm gãy code, không viết hộ đoạn fix; refactor chỉ đổi tên/tách hàm). |
| `codecoach-recap` | Teach-back tối đa 3 câu bằng lời người học + chốt `3 điểm cốt lõi / 1 lỗi tư duy cần tránh` lưu vào `.codecoach/learner-profile.md`. |
| `codecoach-help` | Bảng tra cứu nhanh chế độ, lệnh phanh khẩn cấp, danh sách skill và lối thoát. |

## Chế độ Vận hành & Bộ Lệnh Phanh Khẩn cấp

| Lệnh | Ý nghĩa |
| :--- | :--- |
| `/strict` hoặc `/codecoach strict` | **Strict Study Mode (mặc định):** Học sâu từ gốc — bật đủ cổng `.md`, thang gợi ý 4 tầng, bắt buộc teach-back. |
| `/build` hoặc `/codecoach build` (`guided`) | **Guided Build Mode:** Chạy tiến độ dự án — hỗ trợ boilerplate/config, cho phép blueprint gọn cho hàm nhỏ <=30 dòng; vẫn khóa chặt core logic & bằng chứng debug. |
| `/codecoach open` | Bỏ cổng chặn blueprint/thang gợi ý; vẫn giữ trích nguồn `H4+`, khóa phạm vi và câu hỏi kiểm tra. |
| `/codecoach off` | Tắt gia sư, về trợ lý bình thường (hoặc gõ `"stop codecoach"`). |
| `/focus` | **Phanh khẩn cấp:** Cắt ngay phần lan man, kéo AI quay lại đúng 1 bước hiện tại. |
| `/source` | **Phanh trích nguồn:** Dừng lại và cung cấp `[Nguồn: ... — Vị trí: ...]` hoặc gắn nhãn `[CHƯA KIỂM CHỨNG]`. |

**Lối thoát khi bị kẹt:** Gõ `"I'm stuck"` ("mình bí rồi") để mở tầng gợi ý kế tiếp sau khi đã thử. Gõ `"show the answer"` sau 2 lần thử thực tế ở `strict` (1 lần ở `build`) để mở Tầng 4 — bắt buộc giải thích lại bản chất trước khi qua bước mới.

## Cài đặt & Sử dụng

### 1. Antigravity IDE (Global Skills + MCP Server)
1. Sao chép thư mục `skills/*` vào `~/.gemini/config/skills/` (Windows: `C:\Users\<User>\.gemini\config\skills\`) rồi chạy `Developer: Reload Window`.
2. Khai báo MCP server trong `~/.gemini/config/mcp_config.json`:
   ```json
   "codecoach": {
     "command": "node",
     "args": ["D:/Github/CodeCoach/mcp/server.mjs"]
   }
   ```

### 2. Khởi tạo Hồ sơ Học tập Xuyên phiên (`.codecoach/learner-profile.md`)
```bash
python scripts/personalize.py --init-profile --workspace D:/DuAnCuaBan
```

### 3. Đồng bộ & Kiểm thử Bộ Quy tắc Đa IDE
Khi chỉnh sửa `AGENTS.md` hoặc `skills/*/SKILL.md`, chạy:
```bash
python scripts/sync_rules.py
python scripts/validate.py --release
node tests/mcp-smoke.mjs
```

## Giấy phép

[MIT](LICENSE)
