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

```
# BỘ QUY TẮC BẮT BUỘC: HƯỚNG DẪN HOÀN THÀNH BÁO CÁO BÀI TẬP LỚN

Để đảm bảo cuốn Báo cáo Bài tập lớn cuối kỳ đạt kết quả thẩm định cao nhất từ Hội đồng chuyên môn, toàn bộ các thành viên trong nhóm có trách nhiệm tuyệt đối tuân thủ nghiêm ngặt **04 Quy tắc cốt lõi** dưới đây:

---

## 🛑 Quy tắc 1: Nghiên cứu khung sườn chuẩn hóa
* **Nội dung bắt buộc:** Toàn bộ thành viên phải đọc và nắm rõ cấu trúc báo cáo chi tiết được quy định tại file `docs/complete-report-guide.md` trước khi tiến hành viết nội dung.
* **Yêu cầu:** Mọi đề mục, font chữ, quy cách đánh số hình vẽ/bảng biểu trong file báo cáo cuối cùng phải khớp 100% với khung tài liệu hướng dẫn.

## 👥 Quy tắc 2: Phân rã nhiệm vụ đúng vai trò
Nhóm phải thực hiện phân chia công việc minh bạch theo mô hình 3 nhân sự chính. Tuyệt đối không đùn đẩy trách nhiệm:
* **Sinh viên A (Project Manager & Backend Lead):** Chịu trách nhiệm thiết kế hệ thống, viết API và hoàn thiện Chương 1 & Chương 2 (mục database, kiến trúc tổng thể).
* **Sinh viên B (AI & Data Engineer):** Chịu trách nhiệm thiết kế luồng xử lý Agent, Prompt, kết nối RAG và hoàn thiện Chương 2 (mục LangGraph) & Chương 3 (mục thuật toán).
* **Sinh viên C (Frontend Developer & QA):** Chịu trách nhiệm xây dựng giao diện UI/UX, tích hợp API, thực hiện Test Cases và hoàn thiện Chương 3 (mục tổng quan frontend) & Chương 4.

## 📷 Quy tắc 3: Thu thập minh chứng trong quá trình phát triển (Chụp ảnh/Vẽ sơ đồ)
Nghiêm cấm việc dùng ảnh mạng hoặc tạo dữ liệu giả lập không có trong mã nguồn. Mỗi thành viên có trách nhiệm bàn giao minh chứng số cho cuốn báo cáo theo phân viện:

| Thành viên đảm nhiệm | Danh mục minh chứng bắt buộc phải bàn giao |
| :--- | :--- |
| **Sinh viên A** | <ul><li>Sơ đồ kiến trúc hệ thống tổng thể</li><li>Biểu đồ Use Case tổng quát</li><li>Sơ đồ quan hệ thực thể (ERD Diagram) từ Database thực tế</li></ul> |
| **Sinh viên B** | <ul><li>Sơ đồ khối luồng chạy của LangGraph (State Machine)</li><li>Các đoạn cấu hình System Prompt mẫu</li><li>Bảng số liệu đối sánh kết quả dịch thuật ngữ</li></ul> |
| **Sinh viên C** | <ul><li>Bảng kịch bản kiểm thử (Test Cases) có kết quả cụ thể</li><li>Ảnh chụp màn hình thực tế toàn bộ giao diện ứng dụng (Auth, Dashboard, Workspace, Glossary)</li></ul> |

## 📅 Quy tắc 4: Tích hợp tiến độ song song (Continuous Documentation)
* **Nguyên tắc cốt lõi:** Code đi đôi với Tài liệu. Nghiêm cấm hành vi dồn toàn bộ việc viết báo cáo vào tuần cuối cùng trước hạn nộp.
* **Yêu cầu thực hiện:** Ngay sau khi một Module hoặc Feature được hoàn thiện và test chạy ổn định, thành viên phụ trách phải lập tức viết tài liệu đặc tả, chụp ảnh minh chứng trực quan và cập nhật nội dung đó vào phôi báo cáo chung.

# QUY TẮC COMMIT GIT (RÚT GỌN)

## 🛑 1. Quy tắc 1: Một việc - Một Commit
* Không gộp nhiều tính năng khác nhau vào chung một commit.
* Mỗi lần hoàn thành xong một việc nhỏ (ví dụ: xong giao diện nút bấm, xong một hàm API), hãy commit ngay.

## 📝 2. Quy tắc 2: Viết Message theo chuẩn ngắn gọn
Không viết commit vô nghĩa (như: `fix`, `update`, `abc`). Hãy viết theo cú pháp:
> **`[Tên_Module] Hành động cụ thể`**

* **Ví dụ đúng:**
  * `[Backend] Fix loi het han token JWT`
  * `[Frontend] Sửa giao diện thanh Sidebar`
  * `[AI] Thêm prompt cho Agent Reviewer`

## ⚠️ 3. Quy tắc 3: Luôn Pull trước khi Push
Trước khi đẩy code của mình lên GitHub, bắt buộc phải kéo code mới nhất của nhóm về máy để tránh đè câu lệnh hoặc gây lỗi xung đột (conflict):
1. `git pull origin main` (Kéo code mới về và sửa lỗi xung đột nếu có)
2. `git push origin [ten_nhanh_cua_ban]` (Đẩy code của mình lên)