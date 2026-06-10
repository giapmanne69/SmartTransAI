# BỘ QUY TẮC VÀ HƯỚNG DẪN HOÀN THÀNH BÁO CÁO KHOA HỌC CUỐI KỲ

Tài liệu này cung cấp:
* Khung sườn cấu trúc Bài báo khoa học / Báo cáo nghiên cứu chuẩn hóa (Thay thế hoàn toàn mô hình báo cáo ứng dụng phần mềm).
* Quy trình thiết lập thực nghiệm, thu thập số liệu định lượng ($BLEU$, tỷ lệ lỗi) và phân tích định tính.
* Kế hoạch phân rã nhiệm vụ cho nhóm 3 sinh viên dựa trên việc phát triển mã nguồn Core Engine (chạy trên Script/Notebook).

---

## 1. Thông tin nhóm và đề tài nghiên cứu

### 1.1. Thành viên nhóm thực hiện
* **Nguyễn Thế Giáp (Leader)** - MSSV: B22DCCN251 *(Phụ trách AI Kernel & Thực nghiệm)*
* **Nguyễn Đình Dũng** - MSSV: B22DCCN131 *(Phụ trách Thiết kế thực nghiệm & Cơ sở khoa học)*
* **Phạm Minh Đức** - MSSV: B22DCCN239 *(Phụ trách Đánh giá số liệu & Kết quả toán học)*

### 1.2. Tên đề tài khoa học
**Hệ thống Cộng tác Người - Máy trong Dịch thuật Học thuật Anh - Việt sử dụng Kiến trúc Multi-Tool AI Agent và Tinh chỉnh Mô hình theo Ngữ cảnh**

### 1.3. Chuẩn hóa thông tin biểu mẫu trang bìa
* **Sinh viên thực hiện:** Nguyễn Thế Giáp, Nguyễn Đình Dũng, Phạm Minh Đức
* **Giảng viên hướng dẫn:** [Điền tên Giảng viên]
* **Đơn vị:** Khoa Công nghệ Thông tin - Học viện Công nghệ Bưu chính Viễn thông
* *Hà Nội, tháng 06 năm 2026*

---

## 2. Khung nội dung Bài báo khoa học (Research Paper Structure)

### TÓM TẮT (ABSTRACT)
* **Bối cảnh:** Sự gia tăng mạnh mẽ của tài liệu khoa học quốc tế đòi hỏi hệ thống dịch đạt độ chính xác cao về thuật ngữ. Các công cụ NMT truyền thống và việc gọi LLM theo dạng Zero-shot vẫn gặp hạn chế nghiêm trọng về tính nhất quán ngữ cảnh và bảo toàn cấu trúc dữ liệu tệp (XML/DOM).
* **Bài toán nghiên cứu:** Giảm tải cho người kiểm duyệt dịch thuật (Translation Censor) thông qua việc tự động hóa phát hiện lỗi ngữ nghĩa, tối ưu hóa bộ nhớ dịch thuật (TM) và áp dụng từ điển thuật ngữ chuyên ngành (Glossary) tự động.
* **Giải pháp đề xuất:** Xây dựng Core Engine dịch thuật dựa trên kiến trúc Multi-Tool AI Agent (vận hành bằng LangGraph). Hệ thống tích hợp bộ nhớ trạng thái ngắn hạn (Short-term State Memory), cơ chế RAG dựa trên khoảng cách Cosine trên VectorDB để truy vấn thuật ngữ động, và một bộ kiểm tra lỗi logic học thuật (Error Detection Tool).
* **Kết quả đạt được:** Hệ thống cải thiện rõ rệt chỉ số định lượng ($BLEU$ score), nâng cao tỷ lệ tuân thủ thuật ngữ chuyên ngành và giảm thiểu thời gian hiệu chỉnh của con người (Human-in-the-loop).

---

### CHƯƠNG 1: MỞ ĐẦU (INTRODUCTION)
* **1.1. Đặt vấn đề và động lực nghiên cứu:** Sự cần thiết của việc dịch thuật chính xác tài liệu học thuật (CNTT, Y sinh, Khoa học dữ liệu). Thách thức về tính hệ thống của thuật ngữ trong văn bản dài.
* **1.2. Hạn chế của các nghiên cứu và công cụ hiện tại:** Phân tích hiện tượng ảo tưởng (Hallucination) của LLM; vấn đề trôi ngữ cảnh khi tài liệu bị băm nhỏ cô lập; sự phá vỡ cấu trúc định dạng file khi dịch thô.
* **1.3. Đóng góp khoa học của đề tài:**
    1. Đề xuất quy trình xử lý văn bản song ngữ bảo toàn cấu trúc phân đoạn (`doc_processor`).
    2. Thiết kế và cài đặt kiến trúc Multi-Agent điều khiển bằng đồ thị trạng thái (State Graph).
    3. Tích hợp cơ chế RAG thời gian thực tối ưu hóa độ chính xác của từ điển chuyên ngành.
* **1.4. Bố cục của bài báo khoa học.**

---

### CHƯƠNG 2: TỔNG QUAN CÁC CÔNG NGHỆ LIÊN QUAN (RELATED WORK)
* **2.1. Mô hình ngôn ngữ lớn và Context-aware Translation:** Nguyên lý cửa sổ ngữ cảnh (Context Window) của kiến trúc Transformer giúp xử lý mạch văn dịch thuật.
* **2.2. Kiến trúc RAG (Retrieval-Augmented Generation) và Cơ sở dữ liệu Vector:** Cơ chế Embeddings dữ liệu, nguyên lý toán học của việc tìm kiếm láng giềng gần nhất trên không gian đa chiều (ChromaDB/Qdrant).
* **2.3. Kiến trúc AI Agent và cơ chế Tool Calling:** Phân tích quy trình suy luận ReAct (Reasoning and Acting), cách Agent tương tác với các hàm ngoại vi để kiểm chứng thông tin trước khi xuất bản bản dịch.

---

### CHƯƠNG 3: PHƯƠNG PHÁP NGHIÊN CỨU VÀ THIẾT KẾ CORE ENGINE (METHODOLOGY)
* **3.1. Kiến trúc luồng xử lý AI tập trung (Agentic Workflow Architecture):** Vẽ và mô tả sơ đồ luồng dữ liệu chạy ngầm từ văn bản gốc $\rightarrow$ Trích xuất câu $\rightarrow$ Nhúng Vector $\rightarrow$ Vòng lặp Agent $\rightarrow$ Xuất dữ liệu đối sánh.
* **3.2. Mô hình phân tách văn bản bảo toàn cấu trúc:** Thuật toán phân tích cấu trúc tệp đầu vào, đóng gói văn bản dưới dạng cấu trúc dữ liệu JSON để phục vụ ánh xạ ngược (Reverse Mapping) sau khi dịch:
  $$\text{Chunk}_i = \{\text{TextContent}, \text{ContextWindow}, \text{PositionIndex}\}$$
* **3.3. Thiết kế chi tiết Hệ thống Multi-Agent và Agent Tools:**
    * **Cơ chế quản lý trạng thái Graph:** Định nghĩa bộ nhớ ngắn hạn (Short-term State Memory) để truyền ngữ cảnh dịch từ phân đoạn trước sang phân đoạn sau.
    * **Glossary Retrieval Tool:** Công thức tính toán độ tương đồng Cosine để tự động bốc tách thuật ngữ chuyên ngành từ VectorDB:
      $$\text{Similarity}(Q, V) = \frac{Q \cdot V}{\|Q\| \|V\|}$$
    * **Academic Error Detection Tool:** Thiết kế cấu trúc đầu ra nghiêm ngặt (Structured Output) bằng Pydantic để Agent tự đánh giá và sửa lỗi ngữ nghĩa, lỗi sai thuật ngữ trước khi kết thúc luồng.

---

### CHƯƠNG 4: THIẾT LẬP THỰC NGHIỆM VÀ ĐÁNH GIÁ ĐỊNH LƯỢNG (EXPERIMENTS AND EVALUATION)
*(Chương trọng tâm thay thế cho phần Demo ứng dụng và Test Case phần mềm)*

* **4.1. Thiết lập môi trường thực nghiệm (Experimental Setup):**
    * **Tập dữ liệu thử nghiệm (Dataset):** Mô tả tập mẫu tài liệu học thuật (Anh - Việt) được sử dụng để chạy thử nghiệm, bao gồm số lượng từ, số phân đoạn, và bản dịch đối chứng chuẩn của con người (Ground Truth).
    * **Mô hình nền (Baseline Models):** Cấu hình các tham số môi trường chạy trên Google Colab / Jupyter Notebook (Sử dụng API của GPT-4o, Gemini 1.5 Pro).
* **4.2. Tiêu chí đánh giá khoa học (Evaluation Metrics):** Định nghĩa công thức toán học và cách thức tính toán các chỉ số:
    * Điểm **BLEU** và chỉ số **TER** đánh giá độ tương đồng văn bản.
    * Chỉ số **Glossary Compliance Rate (GCR)** tính toán tỷ lệ phần trăm thuật ngữ chuyên ngành được dịch chính xác theo yêu cầu.
* **4.3. Phân tích kết quả thực nghiệm và Case Study:**
    * **Bảng số liệu đối sánh thực nghiệm:** Trình bày bảng so sánh định lượng kết quả đầu ra giữa dịch thô Zero-shot và hệ thống Multi-Agent Multi-Tool của nhóm.
    * **Phân tích sai sót mẫu (Error Analysis):** Trích dẫn cụ thể một số câu dịch tiêu biểu để chứng minh luồng tự sửa lỗi (Self-Correction) của Agent đã hoạt động hiệu quả như thế nào khi phát hiện ra lỗi thuật ngữ.

---

### KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
### TÀI LIỆU THAM KHẢO (Theo chuẩn IEEE)
### PHỤ LỤC (Chứa mã nguồn Core chính, Đồ thị cấu trúc LangGraph và các System Prompt thô)

---

## 3. Phân công công việc tối ưu cho nhóm 3 sinh viên

Do loại bỏ hoàn toàn phần lập trình ứng dụng Web (Frontend, Full-stack Database), nhiệm vụ của nhóm sẽ tập trung 100% vào phát triển thuật toán Core Engine và viết tài liệu nghiên cứu chuyên sâu:

### 👤 Sinh viên A: Nguyễn Đình Dũng - Khảo sát và Cơ sở khoa học
* **Nhiệm vụ nghiên cứu & thực nghiệm:** 
    * Thu thập, làm sạch và chuẩn hóa tập dữ liệu mẫu (Dataset) song ngữ dùng làm Ground Truth để chạy thực nghiệm.
    * Xây dựng file tri thức nền, bộ từ điển thuật ngữ chuyên ngành (Glossary) định dạng JSON/Excel để nạp vào hệ thống.
* **Nhiệm vụ viết báo cáo:** 
    * Viết **Tóm tắt (Abstract)**, **Chương 1** (Mở đầu, Đặt vấn đề) và **Chương 2** (Tổng quan công nghệ liên quan).
    * Chịu trách nhiệm chính về định dạng tài liệu, chuẩn hóa công thức toán học và danh mục Tài liệu tham khảo theo chuẩn IEEE.

### 👤 Sinh viên B: Nguyễn Thế Giáp (Leader) - Lập trình Core AI Kernel
* **Nhiệm vụ nghiên cứu & thực nghiệm:** 
    * Lập trình toàn bộ thuật toán xử lý dữ liệu bằng Python trên môi trường Notebook (`services/doc_processor.py`).
    * Thiết kế và cấu hình đồ thị trạng thái LangGraph (`agent/graph.py`), thiết lập các Node Agent và viết logic gọi hàm ngoại vi cho các Agent Tools.
    * Hiện thực hóa luồng kết nối RAG với thư viện Vector DB (`services/vector_service.py`).
* **Nhiệm vụ viết báo cáo:** 
    * Viết **Chương 3 (Toàn bộ phần Phương pháp nghiên cứu):** Vẽ sơ đồ khối kiến trúc Agentic Workflow, giải thích logic toán học của cơ chế bộ nhớ ngắn hạn và thuật toán RAG tra cứu thuật ngữ.
    * Cung cấp các đoạn mã nguồn cốt lõi và hệ thống System Prompts để đưa vào phần Phụ lục.

### 👤 Sinh viên C: Phạm Minh Đức - Đánh giá số liệu & Tính toán thực nghiệm
* **Nhiệm vụ nghiên cứu & thực nghiệm:** 
    * Tiếp nhận file kết quả dịch đầu ra từ Sinh viên B. Sử dụng các thư viện tính toán (như `nltk`, `evaluate` hoặc `scikit-learn`) để chạy các đoạn mã đo đạc điểm số $BLEU$, chỉ số lỗi và tỷ lệ khớp từ điển $GCR$.
    * Lập biểu đồ, bảng biểu trực quan hóa sự chênh lệch hiệu năng giữa các phương pháp.
* **Nhiệm vụ viết báo cáo:** 
    * Viết **Chương 4 (Thực nghiệm và Đánh giá):** Thuyết minh chi tiết thông số môi trường cài đặt, diễn giải các bảng số liệu, biểu đồ toán học.
    * Viết phần **Phân tích mẫu sai sót (Case Study)** để chứng minh luận điểm khoa học.
    * Viết phần **Kết luận và Hướng phát triển**.

---

## 4. Tiến độ phối hợp thực hiện (Workflow 6 tuần)

* **Tuần 1:** Thống nhất bài toán $\rightarrow$ Sinh viên A xây dựng tập Dataset nền; Sinh viên B vẽ cấu trúc đồ thị LangGraph; Sinh viên C nghiên cứu các thư viện tính điểm $BLEU$.
* **Tuần 2-3:** Sinh viên B tập trung code hoàn thiện Core AI Engine trên Jupyter Notebook; Sinh viên A hoàn thành Chương 1 và Chương 2 của báo cáo.
* **Tuần 4:** Sinh viên B chạy script dịch thuật trên tập dữ liệu của Sinh viên A, xuất ra file kết quả thô. Sinh viên C lập trình script đo đạc dữ liệu và tính toán điểm số khoa học.
* **Tuần 5:** Sinh viên C viết Chương 4; Sinh viên B viết Chương 3; Sinh viên A tổng hợp phôi, soát lỗi chính tả và quy chuẩn hóa các công thức toán học.
* **Tuần 6:** Tổng duyệt lại toàn bộ các luận điểm khoa học trong báo cáo, chạy thử nghiệm kiểm chứng lần cuối và xuất bản file báo cáo PDF.

---

## 5. Checklist nghiêm ngặt trước khi nộp bài báo
* [ ] Báo cáo không chứa bất kỳ hình ảnh nào liên quan đến giao diện nút bấm (UI/UX) hoặc các test case đăng nhập/đăng ký phần mềm.
* [ ] Mọi biểu đồ, số liệu trong bảng ở Chương 4 phải là kết quả tính toán số học thực tế từ file đầu ra của code Kernel; tuyệt đối không tự "vẽ" số liệu.
* [ ] Các thuật ngữ chuyên ngành (ví dụ: *Context Window, Multi-Agent, Cosine Similarity*) phải sử dụng nhất quán một cách gọi từ đầu đến cuối báo cáo.
* [ ] Tất cả các phương trình toán học (như công thức Cosine Similarity) phải được gõ bằng định dạng LaTeX chuẩn chỉ.
* [ ] Các tài liệu tham khảo phải được trích dẫn nguồn rõ ràng trong nội dung văn bản (ví dụ: `[1]`, `[2]`) và khớp với danh mục tài liệu ở cuối bài.
