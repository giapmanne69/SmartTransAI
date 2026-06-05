# HƯỚNG DẪN HOÀN THÀNH BÁO CÁO BÀI TẬP LỚN CUỐI KỲ

Tài liệu này cung cấp **Cấu trúc chi tiết của cuốn báo cáo** và **Kế hoạch phối hợp thực hiện dành cho nhóm 3 sinh viên** nhằm tối ưu hóa năng suất và đảm bảo tính đồng bộ của dự án Smart Trans AI.

---

## Phần 1: Cấu trúc chi tiết cuốn báo cáo (Khung nội dung)

### TRANG BÌA & MỤC LỤC
### LỜI MỞ ĐẦU

### CHƯƠNG 1: KHẢO SÁT BÀI TOÁN VÀ PHÂN TÍCH YÊU CẦU
* **1.1. Khảo sát thực trạng:** Đánh giá các công cụ dịch thuật hiện tại (Google Translate, DeepL). Hạn chế của dịch thô (Zero-shot LLM) đối với tài liệu dài (mất ngữ cảnh, sai thuật ngữ).
* **1.2. Phân tích yêu cầu chức năng (Functional Requirements):** Đặc tả chi tiết các tính năng: Quản lý tài liệu, Quản lý Glossary/TM, Không gian dịch song ngữ (Workspace), Luồng xử lý Agent tự động.
* **1.3. Yêu cầu phi chức năng (Non-functional Requirements):** Bảo mật (JWT), tốc độ phản hồi, kiến trúc bất đồng bộ xử lý file lớn, giao diện scannable dễ nhìn.
* **1.4. Biểu đồ Use Case:** Vẽ biểu đồ tổng thể chỉ ra tương tác giữa các Tác nhân (User, Admin) và Hệ thống.

### CHƯƠNG 2: THIẾT KẾ KIẾN TRÚC VÀ CƠ SỞ DỮ LIỆU
* **2.1. Kiến trúc tổng thể hệ thống (System Architecture):** Mô tả luồng dữ liệu giữa Frontend React $\leftrightarrow$ Backend FastAPI $\leftrightarrow$ Vector Database & Relational Database.
* **2.2. Thiết kế Cơ sở dữ liệu (Database Design):** * Sơ đồ quan hệ thực thể (ERD Diagram).
    * Đặc tả chi tiết cấu trúc các bảng (`users`, `documents`, `translation_jobs`, `glossaries`,...).
* **2.3. Thiết kế luồng xử lý AI Agent (Agentic Workflow Design):** Sơ đồ khối kiến trúc LangGraph. Giải thích luồng đi của dữ liệu qua từng State và các Node (Translator, Reviewer).

### CHƯƠNG 3: CÀI ĐẶT VÀ HIỆN THỰC HÓA HỆ THỐNG
* **3.1. Môi trường và Công nghệ sử dụng:** Liệt kê phiên bản Python, Node.js, thư viện cốt lõi (FastAPI, LangGraph, SQLAlchemy, React, Tailwind).
* **3.2. Cấu trúc mã nguồn chi tiết:** Giải thích ý nghĩa phân cấp thư mục của dự án (theo cấu trúc MVP+).
* **3.3. Hiện thực hóa các Module cốt lõi (Đoạn code quan trọng và giải thích):**
    * *Module Tiền xử lý (`doc_processor.py`):* Thuật toán tách câu giữ ngữ cảnh.
    * *Module AI Agent (`graph.py`):* Code cấu hình State và quy tắc chuyển hướng (Conditional Routing) giữa các Node Agent.
    * *Module Vector Service (`vector_service.py`):* Code lưu trữ và truy vấn thuật ngữ tương đồng.

### CHƯƠNG 4: THỬ NGHIỆM, ĐÁNH GIÁ VÀ DEMO KẾT QUẢ
* **4.1. Kịch bản kiểm thử (Test Cases):** Bảng kiểm thử các chức năng chính (Auth, Upload, Dịch, Export).
* **4.2. Đánh giá chất lượng dịch thuật của AI:** Đưa ra bảng so sánh kết quả dịch mẫu (Anh -> Việt) giữa hệ thống Smart Trans AI và Google Translate/Dịch thô bằng LLM để làm nổi bật vai trò của Glossary và Agent.
* **4.3. Giao diện demo hệ thống:** Chụp ảnh màn hình thực tế các màn hình ứng dụng (kèm mô tả chức năng từng nút bấm, khu vực trên UI).

### KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
### TÀI LIỆU THAM KHẢO

---

## Phần 2: Hướng dẫn thực hiện và phân chia công việc (Nhóm 3 Sinh viên)

Để hoàn thành khối lượng công việc trên trong vòng 4-6 tuần, nhóm cần phân rã nhiệm vụ chi tiết theo đúng chuyên môn như sau:

### 👤 Sinh viên A: Project Manager & Backend Lead
* **Vai trò chính:** Thiết kế kiến trúc hệ thống, xây dựng Core Backend, quản lý Database và API endpoints.
* **Nhiệm vụ trong Code:**
    * Khởi tạo cấu trúc dự án backend, cấu hình cấu trúc cấu trúc file (`core/config.py`, `database.py`).
    * Thiết kế hệ thống DB Models (`models.py`) và thực hiện migration.
    * Viết các API endpoints phục vụ cho Auth, Document, và Glossary.
* **Nhiệm vụ viết Báo cáo:**
    * Viết **Lời mở đầu** và **Chương 1** (Khảo sát bài toán, Đặc tả yêu cầu chức năng, Vẽ biểu đồ Use Case).
    * Viết **Chương 2 - Mục 2.1 & 2.2** (Vẽ sơ đồ kiến trúc hệ thống tổng thể, vẽ sơ đồ ERD và đặc tả chi tiết các bảng dữ liệu).
    * Chịu trách nhiệm tổng hợp, căn chỉnh format toàn bộ cuốn báo cáo (Font, Word template, Mục lục).

### 👤 Sinh viên B: AI Agent & Data Engineer
* **Vai trò chính:** Hiện thực hóa luồng xử lý AI, cấu hình LangGraph, tích hợp RAG và tối ưu hóa hệ thống Prompt.
* **Nhiệm vụ trong Code:**
    * Viết module xử lý văn bản `services/doc_processor.py` (Parser PDF/Word, Sentence Splitter).
    * Xây dựng cấu trúc LangGraph trong `agent/graph.py`, viết logic cho các Agent Nodes và cấu hình `agent/tools.py`.
    * Kết nối Vector Database thông qua `services/vector_service.py` để làm RAG cho Glossary/TM.
* **Nhiệm vụ viết Báo cáo:**
    * Viết **Chương 2 - Mục 2.3** (Vẽ sơ đồ khối kiến trúc LangGraph, giải thích cơ chế State Machine và tự sửa lỗi của Agent).
    * Viết **Chương 3 - Mục 3.3** (Giải thích các đoạn code cốt lõi về xử lý file, cấu hình Graph và truy vấn Vector DB).
    * Viết **Chương 4 - Mục 4.2** (Thu thập dữ liệu dịch, lập bảng so sánh kết quả dịch và đánh giá định tính chất lượng đầu ra của AI).

### 👤 Sinh viên C: Frontend Developer & QA (Quality Assurance)
* **Vai trò chính:** Xây dựng giao diện người dùng (UI/UX), kết nối API từ Backend và thực hiện kiểm thử hệ thống.
* **Nhiệm vụ trong Code:**
    * Khởi tạo cấu trúc mã nguồn Frontend, cấu hình Router, Context, Axios Client.
    * Hiện thực hóa giao diện các cụm tính năng trong `features/`: Auth, Dashboard, Glossary.
    * Tập trung xây dựng giao diện màn hình `features/workspace/` (giao diện song ngữ chia theo hàng, có cột hiển thị gợi ý từ AI và Glossary động bên cạnh).
* **Nhiệm vụ viết Báo cáo:**
    * Viết **Chương 3 - Mục 3.1 & 3.2** (Tổng hợp công nghệ sử dụng, giải thích sơ đồ cây cấu trúc mã nguồn của cả Backend và Frontend).
    * Viết **Chương 4 - Mục 4.1 & 4.3** (Lập bảng Kịch bản kiểm thử hệ thống; Chụp ảnh toàn bộ giao diện demo thực tế của sản phẩm, viết mô tả chi tiết cho từng màn hình).
    * Viết phần **Kết luận và Hướng phát triển** của đề tài.

---

## 📈 Quy trình phối hợp làm việc nhóm (Workflow)

```text
1: Thống nhất yêu cầu ──> Thiết kế DB & Sơ đồ Agent (Sinh viên A + B)
                                      │
2-3: Code Core API (SV A) <──────┼──────> Code LangGraph & RAG (SV B)
                                      │
3-4: Code UI & Kết nối API (SV C) <┘
                                      │
5: Viết báo cáo theo cấu phần phân chia ──> Ghép phôi & Chuẩn hóa tài liệu