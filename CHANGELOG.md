# Changelog

Tất cả các thay đổi đáng chú ý của dự án Minicahe sẽ được ghi lại trong tệp này.

Định dạng dựa trên [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), và dự án tuân thủ [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Thêm cờ `--preserve-words` cho phép người dùng cấu hình whitelist bảo vệ các từ khóa quan trọng khỏi bộ lọc nén (#12).
- Thêm cờ `--no-acronym` cho phép vô hiệu hóa thuật toán viết tắt (Auto-Acronymizer) nếu cần (#15).
- Thêm Whitelist tự động cho các thuật ngữ công nghệ ngắn (api, id, url, sql, get, put, v.v) nhằm tránh bị xóa nhầm do quy tắc độ dài từ (#14).
- Viết Unit Tests đầy đủ cho `code_compressor.py` và thuật toán `Auto-Acronymizer` để chống lỗi hồi quy (#16, #18).

### Fixed
- **Logic:** Ngăn chặn lỗi "đụng độ từ viết tắt" (Acronym collision) khi tạo ra một từ viết tắt trùng với từ đã có trong văn bản hoặc trùng với một cụm từ khác (#4, #5).
- **Logic:** Ngăn chặn lỗi mất từ lặp lại (Keyword dedup) trên diện rộng bằng cách giới hạn phạm vi deduplication theo từng câu (reset tại các dấu `. ! ?`) (#2, #13).
- **Logic:** Xóa các từ quan trọng (`key`, `use`, `was`) khỏi danh sách `drop_list` mặc định (#1).
- **Code Quality:** Cải tiến thuật toán xóa docstring trong `code_compressor.py` để không xóa nhầm các biến gán chuỗi thông thường (#9).
- **Code Quality:** Chuẩn hóa định dạng số cho `savings_pct` trong `stats.py` (#8).
- **Code Quality:** Xóa ký tự BOM (`\ufeff`) ở đầu các file mã nguồn (#7).
- **Code Quality:** Xóa mã thừa `STRIP_CHARS` (#6).
- **Docs:** Đính chính các tuyên bố mạnh miệng trong `README.md` để trung thực hơn về mặt kỹ thuật (#10, #11).
