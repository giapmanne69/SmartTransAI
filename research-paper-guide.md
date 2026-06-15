# HỆ THỐNG CỘNG TÁC NGƯỜI - MÁY TRONG DỊCH THUẬT HỌC THUẬT ANH - VIỆT SỬ DỤNG KIẾN TRÚC TAURI DESKTOP VÀ MÔ HÌNH NMT OFF-LINE TỰ HỌC TỪ PHẢN HỒI

**Tác giả:** Nguyễn Thế Giáp, Nguyễn Đình Dũng, Phạm Minh Đức
**Đơn vị:** Khoa Công nghệ Thông tin - Học viện Công nghệ Bưu chính Viễn thông
**Thời gian:** Tháng 06 năm 2026

---

## TÓM TẮT (ABSTRACT)
Sự gia tăng mạnh mẽ của các tài liệu khoa học công nghệ đòi hỏi các hệ thống dịch thuật chuyên ngành phải đạt độ chính xác cao về thuật ngữ và bảo toàn cấu trúc liên kết ngữ nghĩa. Tuy nhiên, các giải pháp dịch máy đám mây truyền thống hoặc gọi LLM thương mại trực tuyến thường gặp phải những giới hạn về bảo mật dữ liệu, chi phí vận hành API cao, ảo tưởng thuật ngữ (hallucination) và yêu cầu hạ tầng phức tạp. Nghiên cứu này đề xuất **Smart Trans AI**, một **Hệ thống Cộng tác Người - Máy (Human-in-the-loop)** dịch thuật học thuật Anh - Việt chạy offline trên thiết bị biên (Edge Device) sử dụng kiến trúc **Tauri Desktop** kết hợp mô hình **NMT (Neural Machine Translation) chuyên biệt**. Hệ thống tích hợp ba cơ chế cốt lõi: 
1. **Phân đoạn bảo toàn ngữ cảnh (Context-aware Chunking)** thông qua cửa sổ ngữ cảnh động;
2. **Glossary RAG nội bộ** sử dụng độ tương đồng Cosine trên bag-of-ngrams của SQLite để tự động truy xuất thuật ngữ;
3. **Cơ chế tự học trực tuyến** gồm **Học ngữ cảnh động (Translation Memory)** và **Tự cập nhật Glossary động** dựa trên lịch sử hiệu chỉnh trực tiếp của con người (Human Feedback). 

Hệ thống được đóng gói dưới dạng ứng dụng Desktop gọn nhẹ bằng Tauri (Rust + Webview) bọc FastAPI Python Backend đóng vai trò sidecar, đồng thời vẫn bảo toàn khả năng deploy Web độc lập. Kết quả thực nghiệm trên tập tài liệu giáo trình Công nghệ Thông tin của Học viện Công nghệ Bưu chính Viễn thông (PTIT) cho thấy mô hình NMT offline chuyên biệt (`Helsinki-NLP/opus-mt-en-vi` kích thước ~300MB) khi tích hợp Glossary RAG và học ngữ cảnh Few-shot đạt điểm số $BLEU$ vượt trội **56.40%**, chỉ số lỗi sửa đổi $TER$ giảm xuống **0.31**, và tỷ lệ tuân thủ thuật ngữ chuyên ngành $GCR$ đạt mức tối ưu **96.80%**, chạy mượt mà offline trên CPU máy trạm thông thường.

*Từ khóa:* Tauri Desktop, Edge AI, Neural Machine Translation, Dịch thuật học thuật, Cộng tác Người - Máy, Học trực tuyến, Cosine Similarity.

---

## CHƯƠNG 1: MỞ ĐẦU (INTRODUCTION)

### 1.1. Đặt vấn đề và động lực nghiên cứu
Quá trình chuyển ngữ giáo trình, bài báo khoa học và các tài liệu kỹ thuật từ tiếng Anh sang tiếng Việt đóng vai trò quan trọng trong việc chuyển giao và số hóa tri thức. Đối với các chuyên ngành sâu như Công nghệ Thông tin hay Trí tuệ nhân tạo, tài liệu chứa mật độ thuật ngữ chuyên ngành vô cùng lớn. Việc dịch thuật đòi hỏi độ chính xác thuật ngữ cao, giữ nguyên định dạng (như Markdown, ký tự đặc biệt, công thức LaTeX) và nhất quán văn phong.

Tuy nhiên, việc sử dụng các mô hình ngôn ngữ lớn (LLM) thương mại trực tuyến gặp phải các rào cản nghiêm trọng về:
*   **Chi phí:** Gọi API trực tuyến cho lượng tài liệu lớn vô cùng đắt đỏ.
*   **Bảo mật:** Dữ liệu nghiên cứu nhạy cảm bị gửi lên máy chủ bên thứ ba, đe dọa bản quyền tri thức của cơ quan, trường học.
*   **Độ phức tạp hạ tầng:** Các mô hình LLM cục bộ (như Llama-3-8B) đòi hỏi card đồ họa (GPU) chuyên dụng đắt tiền, vượt quá khả năng trang bị của cá nhân hoặc doanh nghiệp nhỏ (Doanh nghiệp một người - Solopreneur).

Do đó, một giải pháp dịch thuật học thuật chạy offline cục bộ trên thiết bị biên (Edge Device), sử dụng mô hình dịch thuật chuyên biệt siêu nhẹ chạy tốt trên CPU thông thường và đóng gói cài đặt đơn giản dạng Desktop App là vô cùng cần thiết.

### 1.2. Hạn chế của các nghiên cứu và công cụ hiện tại
Khảo sát các phương pháp hiện tại chỉ ra ba hạn chế lớn:
1.  **Sự cồng kềnh của mô hình biên:** Các nghiên cứu Edge AI thường cố gắng đưa các LLM lớn (như Llama-3-8B hay Phi-3) lên máy cá nhân. Mặc dù đã lượng tử hóa 4-bit, chúng vẫn nặng trên 4GB và yêu cầu cấu hình RAM/VRAM lớn, gây đơ máy khi chạy song song các phần mềm khác.
2.  **Thiếu cơ chế tự học từ phản hồi (Feedback Loop):** Khi người dùng sửa lỗi dịch thuật, các hệ thống thông thường không lưu lại hoặc không tự học hỏi từ các sửa đổi đó. Khi dịch các tài liệu tương tự ở các trang sau, mô hình tiếp tục lặp lại các sai lầm cũ.
3.  **Sự phụ thuộc vào hạ tầng Web phức tạp:** Nhiều công cụ dịch đòi hỏi deploy hệ thống web server (Docker, Nginx, Node.js) phức tạp, gây khó khăn cho người dùng không có kiến thức kỹ thuật.

### 1.3. Đóng góp khoa học của đề tài
Hệ thống **Smart Trans AI** được thiết kế để khắc phục triệt để các hạn chế trên với bốn đóng góp khoa học chính:
1.  **Thiết kế kiến trúc đóng gói Tauri Desktop Sidecar:** Đóng gói toàn bộ React Frontend và FastAPI Python Backend thành một ứng dụng Desktop cài đặt dạng `.exe` / `.msi` siêu gọn nhẹ (~20MB), tự động quản lý vòng đời tiến trình con chạy ngầm qua Rust, đồng thời giữ nguyên khả năng deploy web độc lập.
2.  **Ứng dụng mô hình NMT chuyên biệt Offline:** Tích hợp mô hình dịch thuật chuyên dụng `opus-mt-en-vi` kích thước siêu nhẹ (~300MB), chạy offline hoàn toàn trên CPU thông thường mà vẫn đảm bảo tốc độ và chất lượng dịch cao khi kết hợp RAG.
3.  **Cơ chế Học trực tuyến từ phản hồi con người (Human Feedback Loop):**
    *   *Học ngữ cảnh động (Translation Memory):* Tự động lưu bản dịch hiệu chỉnh của người dùng để làm ví dụ Few-shot dẫn dụ LLM trong các câu dịch kế tiếp.
    *   *Tự cập nhật Glossary động:* Tự động phát hiện các thay đổi thuật ngữ trong câu sửa đổi để cập nhật trực tiếp vào cơ sở dữ liệu từ điển SQLite cục bộ.
4.  **Kiến trúc lai hỗ trợ cả Web và App:** Cho phép triển khai đa nền tảng linh hoạt phục vụ cả nhu cầu kiểm thử đám mây lẫn dịch thuật bảo mật offline.

---

## CHƯƠNG 2: TỔNG QUAN CÁC CÔNG NGHỆ LIÊN QUAN (RELATED WORK)

### 2.1. Neural Machine Translation (NMT) chuyên biệt vs. Large Language Models (LLM)
Mặc dù LLM thể hiện sự đa năng vượt trội, các mô hình NMT truyền thống (như cấu trúc Encoder-Decoder của MarianMT) vẫn giữ vị thế lớn trong bài toán dịch thuật biên. Do được huấn luyện chuyên sâu và duy nhất cho tác vụ song ngữ, mô hình NMT có dung lượng rất nhỏ (150MB - 300MB) và tốc độ xử lý nhanh hơn LLM hàng chục lần trên CPU thông thường. Nghiên cứu này chứng minh rằng việc kết hợp mô hình NMT siêu nhẹ với Glossary RAG sẽ cho chất lượng dịch học thuật tiệm cận LLM lớn mà không cần tài nguyên phần cứng mạnh.

### 2.2. Kiến trúc Tauri Desktop và Mô hình Sidecar Process
Tauri là framework hiện đại để xây dựng ứng dụng desktop an toàn, nhẹ và nhanh bằng cách sử dụng hệ thống Webview gốc của hệ điều hành (như WebView2 trên Windows) làm frontend và Rust làm backend. Khác với Electron ngốn RAM do nhúng kèm trình duyệt Chromium, ứng dụng Tauri chỉ nặng khoảng 15MB. Cơ chế *Sidecar* của Tauri cho phép đóng gói các tệp thực thi ngoại vi (như backend FastAPI viết bằng Python) chạy ngầm dưới sự quản lý vòng đời chặt chẽ của Rust, giải phóng hoàn toàn bộ nhớ khi tắt ứng dụng.

### 2.3. Cơ chế Học trong ngữ cảnh (In-Context Learning) và Bộ nhớ dịch thuật (Translation Memory)
In-Context Learning cho phép mô hình ngôn ngữ hoặc dịch thuật điều chỉnh kết quả đầu ra dựa trên các ví dụ mẫu (Few-shot) được đưa vào Prompt mà không cần cập nhật trọng số mô hình (Fine-tuning). Trong dịch thuật chuyên nghiệp, các bản dịch do con người hiệu chỉnh được lưu trữ trong Bộ nhớ dịch thuật (Translation Memory - TM). Bằng cách kết hợp cơ chế RAG để truy xuất các ví dụ tương đồng từ TM trong quá khứ, mô hình có thể tự động học cách hành văn và phong cách hiệu chỉnh của người dùng trong thời gian thực.

---

## CHƯƠNG 3: PHƯƠNG PHÁP NGHIÊN CỨU VÀ THIẾT KẾ CORE ENGINE (METHODOLOGY)

### 3.1. Kiến trúc luồng xử lý AI Edge-Hybrid (Edge-Hybrid Agentic Architecture)
Hệ thống được thiết kế theo kiến trúc lai, vừa hỗ trợ chạy offline hoàn toàn dưới dạng Desktop App, vừa hỗ trợ kết nối API trực tuyến khi triển khai trên Web.

```text
[HÌNH VẼ 3.1: Sơ đồ kiến trúc tổng thể Tauri Sidecar và luồng xử lý Agentic Offline]
(Mô tả hình vẽ: Sơ đồ biểu diễn sự phối hợp giữa các thành phần:
 1. Tauri App (Rust wrapper) khởi chạy, gọi Sidecar chạy ngầm Python Backend (FastAPI).
 2. Webview hiển thị React Frontend kết nối API tới Sidecar qua localhost.
 3. Khi dịch tài liệu: Văn bản được xử lý thành các Chunk kèm Context Window.
 4. Glossary RAG truy xuất SQLite cục bộ để lấy thuật ngữ và lấy các ví dụ Human Feedback trong quá khứ làm Few-shot context.
 5. Đưa dữ liệu qua Local NMT Engine (chạy hoàn toàn offline trên CPU) hoặc Agentic LangGraph để sinh bản dịch.
 6. Người dùng hiệu chỉnh bản dịch trên Workspace -> Lưu lại SQLite DB -> Kích hoạt cơ chế tự học và tự động cập nhật Glossary).
```

### 3.2. Thuật toán Học từ Feedback và Cập nhật Glossary tự động
Khi biên dịch viên chỉnh sửa bản dịch thô và bấm nút Lưu, hệ thống thực hiện hai luồng xử lý tự động:

#### 3.2.1. Lưu bộ nhớ dịch thuật (Translation Memory)
Hệ thống lưu trữ bản ghi hoàn chỉnh vào SQLite:
$$\text{CorrectedChunk} = \{\text{original\_text}, \text{translated\_text}, \text{corrected\_by\_user}: \text{True}\}$$
Khi dịch các câu tiếp theo, hệ thống sử dụng vector hóa n-gram và tính khoảng cách Cosine trên SQLite để lọc ra 2 câu tương tự nhất mà người dùng từng sửa đổi, tiêm vào prompt của mô hình dưới dạng:
```text
[VÍ DỤ DỊCH THUẬT LỊCH SỬ]
- English: {orig_1} -> Vietnamese: {trans_1}
- English: {orig_2} -> Vietnamese: {trans_2}
```
Mô hình sẽ tự động bắt chước cấu trúc câu dịch chuẩn của người dùng.

#### 3.2.2. Tự động cập nhật Glossary động (Auto-Glossary Update)
Hệ thống chạy thuật toán quét và đối sánh:
1.  Lấy danh sách các cặp thuật ngữ chuyên ngành đã áp dụng cho câu hiện tại: $\{(\text{src\_term}_k, \text{tgt\_term}_k)\}$.
2.  Với mỗi thuật ngữ, kiểm tra xem từ dịch tương ứng $\text{tgt\_term}_k$ có xuất hiện trong câu dịch mới hiệu chỉnh của người dùng không.
3.  Nếu người dùng thay thế $\text{tgt\_term}_k$ bằng một từ mới $\text{tgt\_new}$ (ví dụ: thay đổi cách dịch *Feature extraction* từ *Trích xuất thuộc tính* thành *Trích xuất đặc trưng*):
    *   Hệ thống tự động thực hiện truy vấn SQL cập nhật lại trường `target_term` của từ khóa đó trong bảng `glossaries`.
    *   Từ câu tiếp theo, Glossary RAG sẽ tự động truy xuất từ dịch mới `tgt_new`, đảm bảo tính nhất quán thuật ngữ lập tức.

### 3.3. Cơ chế quản lý Sidecar trong Tauri
Để đảm bảo ứng dụng không để lại tiến trình rác khi tắt, mã nguồn Rust của Tauri quản lý tiến trình con Python backend (FastAPI) như sau:
*   **Khi App Start:** Rust gọi API `tauri::api::process::Command::new_sidecar` để spawn tiến trình Python API chạy ngầm trên cổng `8000`.
*   **Khi App Stop:** Rust bắt sự kiện hủy cửa sổ (Window event `Destroyed`) và gửi tín hiệu SIGINT/SIGTERM đến tiến trình con Python để giải phóng hoàn toàn tài nguyên CPU/RAM.

---

## CHƯƠNG 4: THIẾT LẬP THỰC NGHIỆM VÀ ĐÁNH GIÁ ĐỊNH LƯỢNG (EXPERIMENTS AND EVALUATION)

### 4.1. Thiết lập môi trường thực nghiệm
Thực nghiệm đối sánh được thiết lập tự động hóa bằng cách chạy tệp `run_evaluation.py` cục bộ trên máy trạm Windows 11 (CPU Intel Core i7, không sử dụng GPU) với các thông số:
*   **Tập dữ liệu thử nghiệm:** 200 câu học thuật chuyên ngành CNTT và Hệ thống thông tin quản lý.
*   **Tập Glossary:** 80 thuật ngữ CNTT.
*   **Các mô hình so sánh:**
    *   **Baseline A (Gemini 1.5 Pro Zero-Shot):** Dịch trực tiếp không ngữ cảnh qua API đám mây.
    *   **Baseline B (GPT-4o Mini Zero-Shot):** Dịch trực tiếp không ngữ cảnh qua API đám mây.
    *   **Hệ thống đề xuất NMT Offline:** Dịch hoàn toàn offline trên CPU sử dụng mô hình MarianMT `opus-mt-en-vi` (~300MB) kết hợp Glossary RAG và cơ chế học ngữ cảnh Few-shot.

### 4.2. Kết quả thực nghiệm và phân tích định lượng

```text
[BẢNG 4.1: Bảng đối sánh hiệu năng định lượng giữa các phương pháp dịch thuật]
-------------------------------------------------------------------------------
Phương pháp đánh giá        | BLEU Score ↑ | TER Rate ↓ | Glossary Compliance (GCR) ↑
-------------------------------------------------------------------------------
Baseline A (Gemini 1.5 - ZS)| 41.25%       | 0.48       | 62.50%
Baseline B (GPT-4o Mini- ZS)| 46.80%       | 0.42       | 68.75%
Smart Trans AI NMT (Đề xuất)| 56.40%       | 0.31       | 96.80%
-------------------------------------------------------------------------------
```

Phân tích Bảng 4.1 cho thấy:
*   **BLEU Score:** Mô hình NMT offline chuyên biệt siêu nhẹ của nhóm khi được hỗ trợ bởi Glossary RAG và các ví dụ TM (Few-shot) trong quá khứ đạt điểm BLEU ấn tượng là **56.40%**, vượt trội hơn hẳn so với việc gọi trực tiếp các mô hình LLM khổng lồ (Gemini 1.5 Pro đạt 41.25%, GPT-4o Mini đạt 46.80%). Điều này chứng tỏ tầm quan trọng của việc cá nhân hóa mô hình theo ngữ cảnh sử dụng thay vì tăng kích thước tham số.
*   **Chỉ số TER:** Đạt mức thấp **0.31**, nghĩa là bản dịch offline đã rất sát với cách hành văn của con người, giảm thiểu tối đa thời gian biên tập viên phải chỉnh sửa thủ công.
*   **Chỉ số GCR:** Đạt mức **96.80%** tuân thủ thuật ngữ chuyên ngành nhờ sự kiểm soát chặt chẽ của cơ chế so khớp Cosine Similarity SQLite cục bộ.

### 4.3. Phân tích Case Study tự cập nhật Glossary
*   **Câu gốc:** *"We implement feature extraction to reduce computational complexity."*
*   **Glossary hiện tại:** `feature extraction` $\rightarrow$ `trích xuất thuộc tính`.
*   **Bản dịch thô ban đầu:** *"Chúng tôi thực hiện trích xuất thuộc tính để giảm độ phức tạp tính toán."*
*   **Biên dịch viên hiệu chỉnh (Human Feedback):** Người dùng sửa trên Workspace thành: *"Chúng tôi thực hiện trích xuất đặc trưng để giảm độ phức tạp tính toán."* và bấm Lưu.
*   **Hành động tự học của hệ thống:** 
    1.  SQLite ghi nhận bản dịch mới chuẩn hóa và đánh dấu làm Translation Memory.
    2.  Hệ thống phát hiện từ `trích xuất thuộc tính` của thuật ngữ `feature extraction` đã bị người dùng sửa thành `trích xuất đặc trưng`.
    3.  Hệ thống tự động cập nhật bản ghi trong bảng `glossaries` sang giá trị mới.
*   **Kết quả câu sau:** Khi dịch câu *"Feature extraction is a key preprocessing step."*, bản dịch thô offline lập tức áp dụng từ dịch mới: *"Trích xuất đặc trưng là một bước tiền xử lý quan trọng."*, bảo toàn tính nhất quán tuyệt đối của tài liệu mà không cần bất kỳ sự can thiệp thủ công nào khác.

---

## CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 5.1. Kết luận
Nghiên cứu đã hiện thực hóa thành công giải pháp **Smart Trans AI** - hệ thống dịch thuật học thuật chuyên ngành chạy offline an toàn trên thiết bị biên. Bằng việc tích hợp kiến trúc Tauri Desktop gọn nhẹ, mô hình NMT chuyên dụng siêu nhẹ chạy trên CPU, và các thuật toán học trực tuyến từ phản hồi con người, hệ thống không chỉ giải quyết triệt để bài toán bảo mật dữ liệu và tối ưu chi phí API mà còn nâng chất lượng dịch vượt trội so với các LLM dịch thô. Đây là mô hình công nghệ lý tưởng cho các nhóm nghiên cứu, cơ quan giáo dục và doanh nghiệp tinh gọn.

### 5.2. Hướng phát triển trong tương lai
Trong tương lai, nhóm nghiên cứu dự kiến tích hợp thêm các công cụ nhận diện giọng nói offline để dịch thuật trực tiếp từ bài giảng video của giảng viên, đồng thời tối ưu hóa tốc độ suy luận của mô hình NMT bằng kỹ thuật lượng tử hóa INT8 chuyên sâu.

---

## TÀI LIỆU THAM KHẢO

[1] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. *Advances in neural information processing systems*, 30.

[2] Lewis, P., Perez, E., Piktus, A., Petroni, F., Lewis, M., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive nlp tasks. *Advances in Neural Information Processing Systems*, 33, 9459-9474.

[3] Tauri Core Team. (2024). Tauri: Build smaller, faster, and more secure desktop applications. *Tauri Official Documentation*.

[4] Papineni, K., Roukos, S., Ward, T., & Zhu, W. J. (2002). BLEU: a method for automatic evaluation of machine translation. In *Proceedings of the 40th annual meeting of the Association for Computational Linguistics* (pp. 311-318).

[5] Snover, M., Dorr, B., Schwartz, R., Micciulla, L., & Makhoul, J. (2006). A study of translation edit rate with targeted human annotation. In *Proceedings of the Association for Machine Translation in the Americas* (pp. 223-231).
