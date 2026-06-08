## Thành viên nhóm
1. Nguyễn Thế Giáp (Leader) - B22DCCN251
2. Nguyễn Đình Dũng - B22DCCN131
3. Phạm Minh Đức - B22DCCN239

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

```text
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

