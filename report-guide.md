# HƯỚNG DẪN HOÀN THÀNH BÁO CÁO BÀI TẬP LỚN CUỐI KỲ

Tài liệu này cung cấp:

* Cấu trúc chi tiết cho báo cáo đề tài Smart Trans AI.
* Kế hoạch phối hợp cho nhóm 3 sinh viên trong 4–6 tuần.
* Phân công rõ ràng giữa công việc kỹ thuật và viết báo cáo.

## 1. Thông tin nhóm và đề tài

### 1.1. Thành viên

* Nguyễn Đình Dũng - B22DCCN131
* Nguyễn Thế Giáp (Leader) - B22DCCN251
* Phạm Minh Đức - B22DCCN239

### 1.2. Tên đề tài

**Hệ thống Cộng tác Người - Máy trong Dịch thuật Học thuật Anh - Việt sử dụng Kiến trúc Multi-Tool AI Agent và Tinh chỉnh Mô hình theo Ngữ cảnh**

### 1.3. Thông tin biểu mẫu trang bìa

**Sinh viên thực hiện:** [Điền tên nhóm/tên sinh viên]
**Mã số sinh viên:** [Điền MSSV]
**Giảng viên hướng dẫn:** [Điền tên giảng viên]
**Đơn vị:** [Điền tên Trường/Viện]
*Hà Nội, tháng 06 năm 2026*

---

# 2. Khung nội dung báo cáo

# TÓM TẮT (ABSTRACT)

* **Bối cảnh:** Sự gia tăng mạnh mẽ của tài liệu khoa học quốc tế đòi hỏi hệ thống dịch thuật đạt độ chính xác cao về thuật ngữ và ngữ cảnh. Các công cụ NMT truyền thống vẫn gặp hạn chế khi xử lý ngữ cảnh học thuật sâu và thường làm mất định dạng tệp đầu vào.
* **Bài toán nghiên cứu:** Giải quyết quá tải cho người kiểm duyệt dịch thuật (Translation Censor), đảm bảo tính nhất quán thuật ngữ xuyên suốt tài liệu dài, và bảo toàn cấu trúc DOM/XML của tệp.
* **Giải pháp đề xuất:** Xây dựng hệ thống dịch thuật phân quyền dựa trên kiến trúc Multi-Tool AI Agent, tích hợp bộ nhớ ngắn hạn, truy vấn thuật ngữ động qua VectorDB RAG và bộ phát hiện lỗi ngữ nghĩa chuyên ngành. Hệ thống vận hành theo cơ chế Human-in-the-Loop và lưu vết dữ liệu hiệu chỉnh để phục vụ Fine-tuning LLM dài hạn.
* **Kết quả kỳ vọng:** Tối ưu thời gian hiệu chỉnh của chuyên gia, tăng tính nhất quán thuật ngữ và xuất bản tài liệu đầu ra giữ nguyên định dạng gốc.

---

# CHƯƠNG 1: MỞ ĐẦU (INTRODUCTION)

## 1.1. Đặt vấn đề và động lực nghiên cứu

Trong bối cảnh hội nhập và bùng nổ thông tin, nhu cầu chuyển ngữ tài liệu học thuật chuyên ngành (CNTT, Y sinh, Kinh tế - Tài chính) giữa tiếng Anh và tiếng Việt ngày càng cấp thiết. Dịch thuật học thuật đòi hỏi độ chuẩn xác ngữ cảnh cao, tính nhất quán thuật ngữ mang tính hệ thống và khả năng bảo toàn cấu trúc văn bản phức tạp (bảng biểu, sơ đồ, liên kết XML/DOM) của các định dạng PDF, Word, HTML.

## 1.2. Hạn chế của các nghiên cứu và công cụ hiện tại

Các công cụ dịch phổ biến hoặc cách gọi LLM theo cơ chế Zero-shot thường bộc lộ:

* **Ảo tưởng thuật ngữ (Hallucination):** Dịch từ-đối-từ làm sai nghĩa khoa học.
* **Thiếu tính nhất quán:** Cùng một thuật ngữ có thể bị dịch khác nhau ở các phần khác nhau của tài liệu dài.
* **Mất cấu trúc tệp:** Trích xuất văn bản thô để dịch dễ phá vỡ định dạng hiển thị, tốn nhiều công sửa thủ công.

## 1.3. Đóng góp khoa học của đề tài

Đề tài hướng tới 3 đóng góp chính:

1. Đề xuất mô hình cộng tác 3 thành phần theo RBAC: **User → AI Agent → Translation Censor**.
2. Thiết kế **Censor AI Agent** tích hợp Short-term Memory và Tool Calling để hỗ trợ phát hiện lỗi thuật ngữ.
3. Xây dựng **Data Logging Pipeline** lưu vết phản hồi con người, tạo nền tảng dữ liệu vàng cho Fine-tuning LLM bằng QLoRA.

## 1.4. Bố cục báo cáo

1. **Tóm tắt (Abstract):** Bối cảnh, bài toán, giải pháp, kết quả, từ khóa.
2. **Chương 1 - Mở đầu:** Lý do chọn đề tài, mục tiêu, phạm vi, đóng góp.
3. **Chương 2 - Tổng quan công nghệ liên quan:** LLM, RAG, AI Agent, RBAC, Related Work.
4. **Chương 3 - Phương pháp nghiên cứu và thiết kế hệ thống:** Kiến trúc, luồng xử lý, thiết kế Agent, dữ liệu, pipeline huấn luyện/tinh chỉnh.
5. **Chương 4 - Cài đặt, thực nghiệm và đánh giá:**

   * 4.1. Kịch bản kiểm thử hệ thống (Test Cases, kết quả Pass/Fail, tiêu chí).
   * 4.2. Đánh giá chất lượng dịch (đối sánh thuật ngữ, định tính/định lượng).
   * 4.3. Minh chứng giao diện và quy trình vận hành (Auth, Dashboard, Workspace, Glossary).
6. **Kết luận và hướng phát triển:** Tổng kết kết quả, hạn chế, lộ trình mở rộng.
7. **Tài liệu tham khảo:** Trình bày theo IEEE hoặc APA.
8. **Phụ lục:** Hình minh chứng, sơ đồ kiến trúc, Use Case, ERD, Prompt mẫu, bảng Test Case đầy đủ.

**Lưu ý chuẩn hóa:** Mọi hình ảnh, bảng số liệu và mô tả kỹ thuật phải trích xuất từ sản phẩm thực tế của nhóm; không sử dụng dữ liệu giả lập không có trong mã nguồn.

---

# CHƯƠNG 2: TỔNG QUAN CÁC CÔNG NGHỆ LIÊN QUAN (RELATED WORK)

## 2.1. Mô hình ngôn ngữ lớn (LLM) và dịch thuật ngữ cảnh (Context-aware Translation)

Trình bày sự dịch chuyển từ RNN/LSTM sang Transformer. Phân tích cách LLM xử lý Context Window để dịch theo mạch văn bản thay vì từng câu cô lập.

## 2.2. Kiến trúc RAG (Retrieval-Augmented Generation) và cơ sở dữ liệu Vector

Mô tả cơ chế Text Embeddings, nguyên lý truy vấn độ tương đồng ngữ nghĩa trên ChromaDB/Milvus và vai trò của Dynamic Glossary trong chất lượng đầu ra.

## 2.3. Kiến trúc AI Agent và cơ chế Tool Calling

Phân tích tư duy Agent theo ReAct (Reasoning and Acting), cơ chế Function Calling và vai trò của công cụ ngoại vi trong xác thực thông tin trước khi ra quyết định.

## 2.4. Quản lý truy cập theo vai trò (RBAC) và bảo mật dữ liệu

Tổng quan cơ chế JWT, Middleware phân quyền và đảm bảo tính cô lập dữ liệu giữa các nhóm người dùng.

---

# CHƯƠNG 3: PHƯƠNG PHÁP NGHIÊN CỨU VÀ THIẾT KẾ HỆ THỐNG (METHODOLOGY)

## 3.1. Kiến trúc tổng thể hệ thống (System Architecture)

Hệ thống theo hướng dịch vụ, tách rõ tầng giao diện phân quyền và tầng nghiệp vụ AI Core. Luồng RBAC qua Middleware:

* **User:** Upload, theo dõi tiến độ, tải xuống tệp.
* **Translation Censor:** Làm việc tại Censor Workspace, tương tác AI Agent, sửa bản dịch thô, phê duyệt từng Chunk.
* **Admin:** Quản trị tài khoản, tài nguyên hệ thống và cơ sở dữ liệu từ điển gốc.

## 3.2. Mô hình phân tách văn bản bảo toàn cấu trúc (Structure-preserving Document Parser)

Module `parser_service.py` phân tích PDF/Word/HTML thành cấu trúc DOM/XML, trích xuất văn bản kèm Metadata:

[
Chunk_i = {TextContent,\ StyleMetadata,\ PositionIndex}
]

Sau khi dịch và kiểm duyệt, module `exporter_service.py` ánh xạ ngược nội dung mới vào đúng Metadata và vị trí ban đầu để bảo toàn định dạng tệp.

## 3.3. Kiến trúc chi tiết Censor AI Agent

Trọng tâm của hệ thống nằm ở `agent_core.py`, nơi Agent vận hành song hành với Censor.

### 3.3.1. Cơ chế bộ nhớ ngắn hạn (Short-term Memory)

Agent duy trì State Buffer theo từng phiên tài liệu. Mỗi chỉnh sửa/phê duyệt của Censor được ghi vào bộ nhớ này để dùng lại cho các Chunk tiếp theo, qua đó tăng tính nhất quán và giảm lặp lỗi.

### 3.3.2. Thiết kế và vận hành các công cụ (Agent Tools)

Agent kích hoạt 2 công cụ cốt lõi qua Function Calling:

#### Tool 1 - Glossary Retrieval Tool

Trích xuất Named Entities, truy vấn tương đồng Cosine trên VectorDB:

[
Similarity(Q,V)=\frac{Q \cdot V}{|Q| |V|}
]

Trong đó:

* (Q): Vector nhúng của đoạn hiện tại.
* (V): Vector nhúng của tập thuật ngữ trong từ điển.

Đầu ra là danh sách thuật ngữ bắt buộc.

#### Tool 2 - Academic Error Detection Tool

Đối chiếu bản dịch thô với Glossary chuẩn để phát hiện lỗi ngữ nghĩa, sai thuật ngữ hoặc văn phong phi học thuật.

Ví dụ đầu ra JSON:

```json
{
  "has_error": true,
  "error_type": "Terminology Mismatch",
  "wrong_phrase": "Từ dịch sai",
  "suggested_phrase": "Từ đề xuất chuẩn",
  "reason": "Lý do khoa học/ngữ cảnh chuyên ngành"
}
```

---

# CHƯƠNG 4: CÀI ĐẶT, THỰC NGHIỆM VÀ ĐÁNH GIÁ (IMPLEMENTATION AND EVALUATION)

## 4.1. Kịch bản kiểm thử hệ thống (System Test Scenarios)

Xây dựng bộ Test Case cho các luồng:

* Đăng nhập.
* Upload tài liệu.
* Khởi tạo Job dịch.
* Kiểm duyệt trong Workspace.
* Cập nhật Glossary.
* Xuất tệp.

Mỗi Test Case cần có:

* Đầu vào.
* Các bước thực hiện.
* Kết quả kỳ vọng.
* Kết quả thực tế.

## 4.2. Đánh giá chất lượng dịch và tính nhất quán thuật ngữ

Thiết lập bảng đối sánh giữa:

* Bản dịch gốc (không hỗ trợ Agent/RAG).
* Bản dịch của hệ thống Smart Trans AI.

Tiêu chí đánh giá:

* Độ đúng thuật ngữ.
* Độ mạch lạc ngữ cảnh.
* Tỷ lệ lỗi được Censor phát hiện.
* Thời gian hiệu chỉnh trung bình.

## 4.3. Đánh giá giao diện và trải nghiệm vận hành

Trình bày ảnh chụp thực tế cho các màn hình Auth, Dashboard, Workspace, Glossary và mô tả vai trò từng thành phần trong quy trình cộng tác User - AI Agent - Translation Censor.

---

# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

Tổng kết kết quả khoa học - kỹ thuật đã đạt được, các giới hạn hiện tại và đề xuất hướng phát triển tiếp theo: tự động đánh giá chất lượng dịch, Human Feedback Learning, tối ưu chi phí suy luận và hỗ trợ đa ngôn ngữ.

# TÀI LIỆU THAM KHẢO

Liệt kê theo một chuẩn trích dẫn thống nhất (khuyến nghị IEEE hoặc APA), bao gồm bài báo khoa học, tài liệu LLM/RAG/LangGraph, framework và công cụ đã sử dụng.

# PHỤ LỤC

Tổng hợp các minh chứng bổ sung:

* Use Case Diagram.
* ERD.
* Lưu đồ State Machine.
* Prompt mẫu.
* Bảng Test Case đầy đủ.
* Ảnh chụp hệ thống theo từng phiên bản Demo.

---

# 3. Phân công công việc theo thành viên

Để hoàn thành khối lượng công việc trong 4–6 tuần, nhóm phân công như sau:

## 3.1. Nguyễn Đình Dũng - Project Manager và Backend Lead

### Vai trò chính

Thiết kế kiến trúc hệ thống, xây dựng Backend Core, quản lý Database và API Endpoints.

### Nhiệm vụ Code

* Khởi tạo cấu trúc dự án Backend, cấu hình hệ thống (`core/config.py`, `database.py`).
* Thiết kế DB Models (`models.py`) và Migration.
* Xây dựng API cho Auth, Document, Glossary.

### Nhiệm vụ Báo cáo

* Viết Lời mở đầu và Chương 1 (khảo sát bài toán, đặc tả yêu cầu, Use Case).
* Viết Chương 2, mục 2.1 và 2.2 (kiến trúc tổng thể, ERD, đặc tả bảng dữ liệu).
* Tổng hợp và căn chỉnh định dạng toàn bộ báo cáo.

## 3.2. Nguyễn Thế Giáp - AI Agent và Data Engineer

### Vai trò chính

Hiện thực luồng AI, cấu hình LangGraph, tích hợp RAG và tối ưu Prompt.

### Nhiệm vụ Code

* Phát triển `services/doc_processor.py` (Parser PDF/Word, Sentence Splitter).
* Xây dựng Graph trong `agent/graph.py`, Logic Node và `agent/tools.py`.
* Kết nối VectorDB trong `services/vector_service.py` cho Glossary/Translation Memory.

### Nhiệm vụ Báo cáo

* Viết Chương 2, mục 2.3 (sơ đồ khối LangGraph, cơ chế State Machine, tự sửa lỗi).
* Viết Chương 3, mục 3.3 (xử lý file, Graph, truy vấn Vector).
* Viết Chương 4, mục 4.2 (thu thập dữ liệu, đối sánh kết quả dịch, đánh giá chất lượng AI).

## 3.3. Phạm Minh Đức - Frontend Developer và QA

### Vai trò chính

Xây dựng UI/UX, kết nối API và kiểm thử hệ thống.

### Nhiệm vụ Code

* Khởi tạo Frontend, cấu hình Router, Context, Axios Client.
* Hiện thực giao diện cho Auth, Dashboard, Glossary trong `features/`.
* Tập trung màn hình `features/workspace/` (song ngữ theo hàng, cột gợi ý AI, Glossary động).

### Nhiệm vụ Báo cáo

* Viết Chương 3, mục 3.1 và 3.2 (công nghệ sử dụng, cây cấu trúc mã nguồn Backend/Frontend).
* Viết Chương 4, mục 4.1 và 4.3 (bảng Test Scenario, ảnh Demo, mô tả màn hình).
* Viết phần Kết luận và Hướng phát triển.

---

# 4. Quy trình phối hợp làm việc nhóm (Workflow)

```text
Tuần 1: Thống nhất yêu cầu → Thiết kế DB và sơ đồ Agent (SV A + B)
Tuần 2-3: Code Core API (SV A) song song với LangGraph + RAG (SV B)
Tuần 3-4: Code UI và kết nối API (SV C)
Tuần 5: Viết báo cáo theo phần đã phân công
Tuần 6: Ghép nối, chuẩn hóa tài liệu, tổng duyệt Demo
```

# 5. Checklist trước khi nộp

* Nội dung báo cáo đầy đủ theo chương, không thiếu mục.
* Tất cả hình ảnh/bảng biểu là minh chứng thật từ hệ thống.
* Tài liệu tham khảo sử dụng một chuẩn trích dẫn thống nhất.
* Thuật ngữ sử dụng nhất quán giữa Code, giao diện và báo cáo.
* Đã soát lỗi chính tả, định dạng, mục lục, danh mục hình/bảng.
* Đã tổng duyệt Demo và đối chiếu với các Test Case trong Chương 4.
