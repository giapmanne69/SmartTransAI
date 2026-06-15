## Thành viên nhóm
1. Nguyễn Thế Giáp (Leader) - B22DCCN251
2. Nguyễn Đình Dũng - B22DCCN131
3. Phạm Minh Đức - B22DCCN239

# Smart Trans AI - Hệ thống Dịch thuật Thông minh ứng dụng Tauri Desktop & NMT Cục bộ

## 📌 Giới thiệu dự án
**Smart Trans AI** là một hệ thống hỗ trợ dịch thuật học thuật chuyên ngành (Computer-Assisted Translation - CAT Tool thế hệ mới) được thiết kế lai (hybrid), hỗ trợ vận hành song song trên môi trường Web đám mây hoặc đóng gói thành phần mềm Desktop offline an toàn trên thiết bị biên.

Hệ thống ứng dụng mô hình dịch thuật chuyên biệt **NMT (Neural Machine Translation) cục bộ** (`opus-mt-en-vi` dung lượng siêu nhẹ ~300MB) chạy mượt mà hoàn toàn offline trên CPU thông thường mà không cần GPU đắt đỏ, kết hợp với cơ chế RAG thuật ngữ thông minh và vòng lặp tự học trực tuyến từ phản hồi con người:
*   **Tích hợp Tauri Desktop (Rust + Webview):** Sử dụng Rust làm cầu nối bảo mật bọc ngoài React Frontend, tự động khởi chạy và quản lý vòng đời của FastAPI Python backend dưới dạng tiến trình con chạy ngầm (Sidecar), giải phóng hoàn toàn bộ nhớ khi tắt app.
*   **Học ngữ cảnh động (Translation Memory):** Tự động lưu lại các bản dịch được con người hiệu chỉnh làm ví dụ Few-shot trong ngữ cảnh dịch của các câu tiếp theo, giúp mô hình bắt chước văn phong và tự sửa lỗi thói quen.
*   **Tự cập nhật Glossary động (Auto-Glossary Update):** Tự động nhận diện sự thay đổi từ dịch thuật ngữ chuyên ngành do người dùng sửa đổi trực tiếp để cập nhật ngược lại SQLite database cục bộ, áp dụng ngay lập tức cho các câu sau.
*   **Bảo toàn định dạng tài liệu:** Giữ nguyên 100% định dạng in đậm, in nghiêng, công thức toán học LaTeX, các bảng biểu và ký tự đặc biệt của file gốc.

---

## 📂 Cấu trúc dự án (Hybrid)
Dự án được thiết kế phân lớp và hỗ trợ cả đóng gói Tauri sidecar:

```text
smart-trans-ai/
│
├── backend/                         # Backend Source Code (FastAPI + SQLite)
│   ├── app/
│   │   ├── main.py                  # Khởi tạo FastAPI, CORS, serving static
│   │   ├── core/                    # Cấu hình hệ thống (Config, Security, Settings)
│   │   ├── database.py              # Quản lý DB Session
│   │   ├── models.py                # Định nghĩa DB Models (User, Doc, Chunk, Glossary)
│   │   ├── api/                     # Tiếp nhận Requests (auth, document, glossary)
│   │   ├── services/
│   │   │   ├── doc_processor.py     # Tiền xử lý tài liệu (PDF/Word/TXT)
│   │   │   ├── vector_service.py    # RAG đối sánh Cosine Similarity trên SQLite
│   │   │   └── nmt_service.py       # [NEW] Mô hình dịch thuật NMT offline cục bộ
│   │   └── llm_provider.py          # Quản lý kết nối LLM (Gemini, Llama-3, OPUS-MT)
│   ├── requirements.txt             # Các thư viện Python cần thiết
│   └── run_desktop.py               # Điểm bắt đầu khởi chạy backend cục bộ
│
├── frontend/                        # Frontend Source Code (React.js + Vite)
│   ├── src/
│   │   ├── components/              # UI Components dùng chung
│   │   ├── features/                # Chia thư mục theo cụm tính năng (auth, workspace...)
│   │   └── main.jsx
│   └── src-tauri/                   # [NEW] Thư mục cấu hình Tauri Desktop App (Rust)
│       ├── src/main.rs              # Rust code quản lý spawn/kill sidecar Python backend
│       ├── Cargo.toml               # Quản lý dependency của Tauri app
│       └── tauri.conf.json          # Cấu hình ứng dụng Tauri (Window size, Sidecar externalBin...)
│
├── data/                            # Thư mục chứa tài nguyên thực nghiệm
│   ├── input_academic.txt           # File câu gốc CNTT kiểm thử
│   ├── glossary.json                # Từ điển thuật ngữ CNTT mẫu
│   ├── ground_truth.json            # Bản dịch đối chứng chuẩn của con người
│   └── evaluation_results.md        # Báo cáo kết quả BLEU, TER, GCR thực tế
│
├── build_desktop.py                 # Script tự động đóng gói FastAPI + React + Tauri thành app cài đặt
├── run_evaluation.py                # Script chạy thực nghiệm tự động
└── README.md                        # Hướng dẫn dự án
```

---

## 🛠️ Yêu cầu chuẩn bị môi trường

### 1. Dành cho Backend & Frontend Web
*   Python 3.10 trở lên
*   Node.js 18 trở lên (đã tích hợp npm)

### 2. Dành cho phát triển Desktop App sử dụng Tauri
Ứng dụng Tauri yêu cầu trình biên dịch Rust để build mã nguồn hệ thống:
*   **Windows:** Tải và cài đặt Rustup thông qua [rustup.rs](https://rustup.rs). Ngoài ra cần cài đặt gói công cụ build của C++ thông qua Visual Studio Build Tools (chọn C++ build tools).

---

## 🚀 Hướng dẫn khởi chạy dự án (3 cách)

Hệ thống hỗ trợ 3 cách chạy chính tùy theo mục đích phát triển và kiểm thử:

---

### CÁCH 1: Khởi chạy Web Client & FastAPI Server (Web Developer Mode)
Dành cho lập trình viên muốn deploy web, chỉnh sửa code hot-reload cho cả backend và frontend.

#### Bước 1: Cấu hình biến môi trường
Tạo file `.env` tại thư mục `/backend` (sử dụng nội dung từ mẫu dưới đây):
```env
DATABASE_URL=sqlite:///./smart_trans.db
JWT_SECRET=supersecretjwtkeychangeinproduction12345
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Cấu hình OpenRouter API phục vụ chế độ dịch hybrid online
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=google/gemini-2.5-pro
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

#### Bước 2: Khởi chạy Backend FastAPI
1. Mở terminal mới, di chuyển vào thư mục backend:
   ```bash
   cd backend
   ```
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
3. Khởi chạy server API:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
*API docs tương tác sẽ tự động hiển thị tại:* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

#### Bước 3: Khởi chạy Frontend React (Vite)
1. Mở terminal song song khác, di chuyển vào thư mục frontend:
   ```bash
   cd frontend
   ```
2. Cài đặt các package:
   ```bash
   npm install
   ```
3. Chạy client ở chế độ phát triển:
   ```bash
   npm run dev
   ```
4. Truy cập giao diện chính của hệ thống tại: [http://localhost:5173](http://localhost:5173)

---

### CÁCH 2: Khởi chạy môi trường phát triển Desktop (Tauri Developer Mode)
Dành cho lập trình viên muốn chạy thử nghiệm trực tiếp cửa sổ ứng dụng Desktop cục bộ và kiểm tra tính tương thích của Webview với OS.

1.  Đảm bảo đã chạy và bật Backend FastAPI ở cổng `8000` (như ở Cách 1).
2.  Di chuyển vào thư mục frontend:
    ```bash
    cd frontend
    ```
3.  Chạy ứng dụng Tauri ở chế độ phát triển:
    ```bash
    npm run tauri dev
    ```
4.  Cửa sổ Desktop của ứng dụng **Smart Trans AI** sẽ tự động hiển thị trực quan mà không cần mở trình duyệt web.

---

### CÁCH 3: Đóng gói ứng dụng Desktop (.exe cài đặt hoàn chỉnh)
Dành cho việc đóng gói bản phân phối release độc lập dạng file cài đặt, tự động bọc backend FastAPI làm sidecar tiến trình con.

1.  Tại thư mục gốc của dự án, mở terminal PowerShell và chạy lệnh:
    ```bash
    python build_desktop.py
    ```
2.  **Quy trình đóng gói tự động:**
    *   Build React frontend thành file tĩnh trong thư mục `frontend/dist`.
    *   Build backend Python thành file thực thi sidecar bằng PyInstaller và tự động copy vào thư mục `frontend/src-tauri/src/bin`.
    *   Gọi Rust Compiler biên dịch mã nguồn Tauri thành file chạy desktop cài đặt hoàn chỉnh.
3.  **Kết quả đầu ra:** Gói cài đặt `.msi` hoặc `.exe` sẽ được tạo ra tại thư mục `frontend/src-tauri/target/release/bundle/`. 
4.  Tải và cài đặt file này trên Windows, ứng dụng sẽ chạy offline hoàn toàn độc lập, tự động bật/tắt FastAPI backend ngầm mỗi khi bạn mở/đóng app.

---

## 🧪 Kịch bản chạy thực nghiệm đối sánh tự động (Evaluation Script)

Để đo đạc BLEU, TER, và tỷ lệ tuân thủ Glossary (GCR) thực tế của mô hình NMT cục bộ so với các baseline dịch thô trực tuyến:

1.  Đảm bảo đã điền API Key trong `/backend/.env`.
2.  Mở terminal tại thư mục gốc của dự án và chạy:
    ```bash
    python run_evaluation.py
    ```
3.  Script sẽ tự động kiểm tra, cài đặt các thư viện còn thiếu và tiến hành dịch thuật 3 phương pháp song song. Kết quả bảng số liệu thực nghiệm đối sánh chi tiết sẽ được hiển thị trực tiếp và lưu tại file `data/evaluation_results.md`.
