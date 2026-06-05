# Smart Trans AI - Hệ thống Dịch thuật Thông minh ứng dụng AI Agent

## 📌 Giới thiệu dự án
**Smart Trans AI** là một hệ thống hỗ trợ dịch thuật thông minh (Computer-Assisted Translation - CAT Tool thế hệ mới) được thiết kế nhằm tối ưu hóa quá trình dịch thuật tài liệu chuyên ngành (Anh - Việt). 

Không giống như các công cụ dịch thuật truyền thống dịch "thô" từng câu đơn lẻ, Smart Trans AI ứng dụng kiến trúc **Multi-Agent (LangGraph)** kết hợp kỹ thuật **RAG (Retrieval-Augmented Generation)** để tự động hóa quy trình:
* **Trích xuất & Tiền xử lý:** Tự động parse tài liệu (PDF/Word), cắt nhỏ văn bản thành các câu (`Chunking`) nhưng vẫn giữ nguyên cửa sổ ngữ cảnh xung quanh để tránh mất nghĩa.
* **Hệ thống AI Tác nhân Đa tầng (Multi-Agent):** Điều khiển luồng dịch qua các Agent chuyên biệt: *Translator Agent* (Dịch thô dựa trên ngữ cảnh) $\rightarrow$ *Reviewer Agent* (Kiểm tra lỗi chính tả, ngữ pháp, độ mượt văn phong) $\rightarrow$ *Style/Alignment Agent* (Đảm bảo định dạng).
* **Đồng bộ Bộ nhớ Dịch thuật (Translation Memory) & Thuật ngữ (Glossary):** Sử dụng Vector Database để tra cứu và áp dụng chính xác các thuật ngữ chuyên ngành theo thời gian thực, đảm bảo tính nhất quán trên toàn bộ tài liệu dài.

Dự án được xây dựng với kiến trúc **MVP+ (Minimum Viable Product Plus)**, phân tách mô-đun rõ ràng, sẵn sàng mở rộng và tối ưu hóa chi phí vận hành API.

---

## 📂 Cấu trúc dự án (MVP+)
Dự án được tổ chức theo mô hình phẳng, gom cụm theo tính năng (Feature-based) ở Frontend và phân lớp nghiệp vụ ở Backend giúp tăng tốc độ phát triển trong giai đoạn đầu:

```mermaid
smart-trans-ai/
│
├── backend/                         # Backend Source Code (FastAPI)
│   ├── app/
│   │   ├── main.py                  # Khởi tạo FastAPI, CORS, include routers
│   │   ├── core/                    # Cấu hình hệ thống (Config, Security, Constants)
│   │   ├── database.py              # Quản lý DB Session và Base Model
│   │   ├── models.py                # Định nghĩa toàn bộ các DB Models (User, Doc, Job, Glossary)
│   │   ├── schemas.py               # Định nghĩa các Pydantic Schemas (Validation dữ liệu)
│   │   ├── api/                     # Nơi tiếp nhận Request (auth.py, document.py, glossary.py)
│   │   ├── services/                # Logic nghiệp vụ (doc_processor.py, vector_service.py,...)
│   │   ├── agent/                   # Hệ thống AI Agent (graph.py, prompts.py, tools.py)
│   │   └── llm_provider.py          # Factory quản lý kết nối LLM (OpenAI, Gemini, Ollama)
│   ├── tests/                       # Unit test hệ thống
│   └── requirements.txt             # Các thư viện Python cần thiết
│
├── frontend/                        # Frontend Source Code (React.js)
│   ├── src/
│   │   ├── components/              # UI Components dùng chung (Button, Modal, Input...)
│   │   ├── features/                # Chia thư mục theo cụm tính năng cốt lõi (Mô hình Feature-based)
│   │   │   ├── auth/                # Trang Đăng nhập, Đăng ký
│   │   │   ├── dashboard/           # Giao diện quản lý danh sách tài liệu
│   │   │   ├── workspace/           # Không gian dịch thuật song ngữ, gợi ý AI, Glossary
│   │   │   └── glossary/            # Giao diện quản lý bộ từ điển thuật ngữ
│   │   ├── services/                # Axios API Client kết nối sang Backend
│   │   ├── App.jsx
│   │   └── main.jsx
│
└── docs/                            # Tài liệu dự án và báo cáo
    ├── api_spec.md                  # Tài liệu đặc tả API
    ├── database_design.md           # Tài liệu thiết kế DB
    └── complete-report-guide.md     # Hướng dẫn và cấu trúc bài tập lớn cuối kỳ

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