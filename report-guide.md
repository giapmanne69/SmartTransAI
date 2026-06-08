# HƯỚNG DẪN HOÀN THÀNH BÁO CÁO BÀI TẬP LỚN CUỐI KỲ

Tài liệu này cung cấp **Cấu trúc chi tiết của cuốn báo cáo** và **Kế hoạch phối hợp thực hiện dành cho nhóm 3 sinh viên** nhằm tối ưu hóa năng suất và đảm bảo tính đồng bộ của dự án Smart Trans AI.

## Phân role theo thành viên
* Nguyễn Đình Dũng - B22DCCN131
* Nguyễn Thế Giáp (Leader) - B22DCCN251
* Phạm Minh Đức - B22DCCN239

# Hệ thống Cộng tác Người – Máy trong Dịch thuật Học thuật Anh – Việt Sử dụng Kiến trúc Multi-Tool AI Agent và Tinh chỉnh Mô hình theo Ngữ cảnh

**Sinh viên thực hiện:** [Tên của bạn]  
**Mã số sinh viên:** [MSSV của bạn]  
**Giảng viên hướng dẫn:** [Tên giảng viên]  
**Đơn vị:** [Tên Trường/Viện]  
*Hà Nội, Tháng 06 Năm 2026*

---

## TÓM TẮT (ABSTRACT)

*   **Bối cảnh:** Sự gia tăng mạnh mẽ của tài liệu khoa học quốc tế đòi hỏi các hệ thống dịch thuật phải đạt độ chính xác cao về mặt thuật ngữ và ngữ cảnh. Tuy nhiên, các công cụ dịch tự động dựa trên kiến trúc Neural Machine Translation (NMT) truyền thống hiện nay thường thất bại trong việc xử lý ngữ cảnh học thuật sâu sắc và làm mất định dạng cấu trúc nguyên bản của file đầu vào.
*   **Bài toán nghiên cứu:** Giải quyết tình trạng quá tải cho người kiểm duyệt dịch thuật (Translation Censor), đảm bảo tính nhất quán thuật ngữ xuyên suốt các tài liệu dài, và bảo toàn toàn vẹn định dạng cấu trúc DOM/XML của các tệp tin.
*   **Giải pháp đề xuất:** Nghiên cứu và xây dựng một hệ thống dịch thuật phân quyền dựa trên kiến trúc Multi-Tool AI Agent. Agent được trang bị bộ nhớ ngắn hạn (Short-term Memory), công cụ truy vấn thực thể động trên cơ sở dữ liệu Vector (VectorDB RAG), và bộ phát hiện lỗi ngữ nghĩa chuyên ngành. Hệ thống hoạt động theo cơ chế cộng tác song hành với con người (Human-in-the-loop), đồng thời lưu vết dữ liệu hiệu chỉnh làm tài nguyên phục vụ tinh chỉnh (Fine-tuning) mô hình LLM cốt lõi dài hạn.
*   **Kết quả:** Hệ thống giúp tối ưu hóa thời gian hiệu chỉnh của chuyên gia dịch thuật, nâng cao tính nhất quán của thuật ngữ chuyên ngành chuyên sâu, và xuất bản tài liệu đầu ra trùng khớp định dạng gốc của tệp tin đầu vào.

---

## CHƯƠNG 1: MỞ ĐẦU (INTRODUCTION)

### 1.1. Đặt vấn đề và Động lực nghiên cứu
Trong kỷ nguyên bùng nổ thông tin và hội nhập toàn cầu, nhu cầu tiếp cận và chuyển ngữ các tài liệu học thuật chuyên ngành (Công nghệ thông tin, Y sinh, Kinh tế - Tài chính) từ tiếng Anh sang tiếng Việt và ngược lại là cực kỳ cấp thiết. Dịch thuật học thuật không chỉ dừng lại ở việc chuyển đổi ngôn từ mà đòi hỏi khắt khe về độ chuẩn xác ngữ cảnh, tính nhất quán mang tính hệ thống của các thuật ngữ chuyên sâu, và khả năng bảo toàn cấu trúc văn bản phức tạp (bảng biểu, sơ đồ, liên kết XML/DOM) của các định dạng tệp phổ biến như PDF, Word, HTML.

### 1.2. Hạn chế của các nghiên cứu và công cụ hiện tại
Các công cụ dịch thuật phổ biến (Google Translate, Microsoft Translator) hoặc việc gọi trực tiếp các mô hình ngôn ngữ lớn (LLM) theo cơ chế Zero-shot thường bộc lộ những hạn chế lớn sau:
*   **Hiện tượng ảo tưởng thuật ngữ (Hallucination):** Dịch thuật từ-đối-từ làm mất đi ý nghĩa khoa học của cụm từ chuyên ngành.
*   **Thiếu tính nhất quán:** Cùng một thuật ngữ chuyên môn ở chương trước có thể bị dịch thành một từ hoàn toàn khác ở chương sau trong một tài liệu dài.
*   **Mất cấu trúc tệp:** Việc trích xuất text thô (raw text) để dịch làm phá vỡ hoàn toàn định dạng hiển thị, gây tốn kém thời gian định dạng lại thủ công.

### 1.3. Đóng góp khoa học của đề tài
Nghiên cứu này đóng góp một giải pháp toàn diện bao gồm:
1.  Đề xuất mô hình phân quyền cộng tác ba thành phần dựa trên vai trò (Role-based Access Control - RBAC) tối ưu hóa luồng công việc giữa **User** (Người cần dịch) $\rightarrow$ **AI Agent** (Trợ lý ảo duyệt tự động) $\rightarrow$ **Translation Censor** (Chuyên gia duyệt tối hậu).
2.  Thiết kế kiến trúc **Censor AI Agent** tích hợp bộ nhớ ngắn hạn (Short-term Memory) quản lý trạng thái hội thoại và cơ chế gọi công cụ (Tool Calling) để tự động hóa việc phát hiện lỗi dịch thuật thuật ngữ.
3.  Xây dựng hệ thống **Data Logging Pipeline** lưu vết chu trình phản hồi của con người, tạo tiền đề xây dựng bộ dữ liệu "vàng" (Gold Standard Dataset) cho việc tinh chỉnh (Fine-tuning) LLM độc lập bằng kỹ thuật QLoRA.

### 1.4. Bố cục của báo cáo khoa học

---

## CHƯƠNG 2: TỔNG QUAN CÁC CÔNG NGHỆ LIÊN QUAN (RELATED WORK)

### 2.1. Mô hình ngôn ngữ lớn (LLM) và Dịch thuật ngữ cảnh (Context-aware Translation)
Tổng quan về sự dịch chuyển từ kiến trúc RNN/LSTM sang kiến trúc Transformer. Phân tích cách các mô hình LLM hiện đại xử lý cửa sổ ngữ cảnh (Context Window) để thực hiện biên dịch dựa trên mạch văn thay vì dịch từng câu cô lập.

### 2.2. Kiến trúc RAG (Retrieval-Augmented Generation) và Cơ sở dữ liệu Vector
Nghiên cứu cơ chế nhúng văn bản (Text Embeddings) để biến các cặp thuật ngữ học thuật thành các vector đa chiều. Phân tích nguyên lý hoạt động của các hệ quản trị cơ sở dữ liệu vector (ChromaDB, Milvus) trong việc tra cứu độ tương đồng ngữ nghĩa phục vụ việc cung cấp từ điển động (Dynamic Glossary) cho mô hình sinh chữ.

### 2.3. Kiến trúc AI Agent và Cơ chế gọi công cụ (Tool Calling)
Phân tích mô hình suy nghĩ của Agent dựa trên các framework như ReAct (Reasoning and Acting). Khảo sát cách thức LLM sinh ra các chuỗi lệnh cấu trúc (Function Calling) để kích hoạt các đoạn mã ngoại vi nhằm kiểm chứng thông tin trước khi ra quyết định.

### 2.4. Quản lý truy cập dựa trên vai trò (RBAC) và Bảo mật dữ liệu
Tổng quan về kiến trúc phân quyền hệ thống dựa trên token JWT (JSON Web Token), đảm bảo tính cô lập dữ liệu và toàn vẹn tài nguyên giữa các nhóm người dùng trong hệ thống cộng tác.

---

## CHƯƠNG 3: PHƯƠNG PHÁP NGHIÊN CỨU & THIẾT KẾ HỆ THỐNG (METHODOLOGY)

### 3.1. Kiến trúc tổng thể hệ thống (System Architecture)
Hệ thống được thiết kế theo mô hình kiến trúc hướng dịch vụ, chia tách rõ ràng giữa tầng giao diện phân quyền và tầng nghiệp vụ AI core. Luồng kiểm soát truy cập dựa trên vai trò (RBAC) được siết chặt qua các Middleware để điều phối tài nguyên:
*   **User:** Chỉ có quyền truy cập các endpoint upload, theo dõi tiến độ và download tệp tin.
*   **Translation Censor:** Có quyền truy cập không gian làm việc chung (Censor Workspace), tương tác với AI Agent, chỉnh sửa bản dịch thô và phê duyệt chunk văn bản.
*   **Admin:** Toàn quyền quản trị tài khoản, kiểm soát tài nguyên hệ thống và quản lý cơ sở dữ liệu từ điển gốc.

### 3.2. Mô hình phân tách văn bản bảo toàn cấu trúc (Structure-preserving Document Parser)
Để giải quyết bài toán mất định dạng file, hệ thống cài đặt module `parser_service.py`. Module này thực hiện phân tách tệp (PDF, Word, HTML) thành dạng cây phân cấp (DOM Tree hoặc cấu trúc XML). Quá trình phân tách trích xuất văn bản thô đồng thời đính kèm một ánh xạ siêu dữ liệu (Metadata Mapping Key):

$$\text{Chunk}_i = \{ \text{TextContent}, \text{StyleMetadata}, \text{PositionIndex} \}$$

Sau khi văn bản thô đi qua luồng dịch thuật và kiểm duyệt, hệ thống gọi `exporter_service.py` để map ngược lại `TextContent` mới vào đúng `StyleMetadata` và `PositionIndex` ban đầu, đảm bảo tệp đầu ra trùng khớp định dạng gốc.

### 3.3. Kiến trúc Chi tiết Censor AI Agent
Trọng tâm khoa học của hệ thống nằm ở module `agent_core.py`, xây dựng một thực thể AI Agent kiểm duyệt hoạt động song hành cùng Censor người.

#### A. Cơ chế Bộ nhớ ngắn hạn (Short-term Memory)
Agent duy trì một bộ đệm trạng thái liên tục (State Buffer) xuyên suốt một phiên làm việc (Session) đối với một tài liệu cụ thể. Khi Censor người thực hiện chỉnh sửa hoặc phê duyệt một thuật ngữ ở đoạn văn bản trước, thay đổi này sẽ ngay lập tức được ghi vào bộ nhớ ngắn hạn của Agent. Ở các đoạn văn bản tiếp theo, Agent dựa vào trạng thái bộ nhớ này để đưa ra các góp ý mang tính nhất quán cao, giảm thiểu việc lặp lại các lỗi sai tương tự.

#### B. Thiết kế và vận hành các Công cụ chuyên biệt (Agent Tools)
Agent được cấp quyền kích hoạt 2 công cụ cốt lõi thông qua cơ chế Function Calling:

*   **Tool 1: Glossary Retrieval Tool (Công cụ truy vấn thuật ngữ):** Khi nhận được một phân đoạn văn bản thô cần dịch hoặc cần duyệt, Tool 1 tự động trích xuất các thực thể danh từ (Named Entities) và thực hiện tìm kiếm tương đồng Cosine (Cosine Similarity) trên VectorDB:

$$\text{Similarity}(Q, V) = \frac{Q \cdot V}{\|Q\| \|V\|}$$

> *Trong đó $Q$ là vector nhúng của đoạn văn bản hiện tại, và $V$ là vector nhúng của tập thuật ngữ có trong cơ sở dữ liệu từ điển.* Đầu ra của Tool 1 là danh sách các thuật ngữ bắt buộc phải tuân theo trong phân đoạn đó.

*   **Tool 2: Academic Error Detection Tool (Công cụ phát hiện lỗi học thuật):** Nhận đầu vào là [Bản dịch thô ban đầu] kết hợp với [Danh sách thuật ngữ chuẩn từ Tool 1]. Tool 2 thực hiện phân tích cú pháp, đối chiếu chéo để phát hiện các lỗi sai về ngữ nghĩa, thuật ngữ chuyên ngành hoặc văn phong phi học thuật. Đầu ra của công cụ này được cấu trúc hóa nghiêm ngặt dưới dạng JSON để phục vụ việc hiển thị ở giao diện:

```json
{
  "has_error": true,
  "error_type": "Terminology Mismatch",
  "wrong_phrase": "Từ dịch sai",
  "suggested_phrase": "Từ đề xuất chuẩn",
  "reason": "Lý do khoa học/ngữ cảnh chuyên ngành"
}

## Phần 2: Hướng dẫn thực hiện và phân chia công việc (Nhóm 3 Sinh viên)

Để hoàn thành khối lượng công việc trên trong vòng 4-6 tuần, nhóm cần phân rã nhiệm vụ chi tiết theo đúng chuyên môn như sau:

### 👤 Nguyễn Đình Dũng: Project Manager & Backend Lead
* **Vai trò chính:** Thiết kế kiến trúc hệ thống, xây dựng Core Backend, quản lý Database và API endpoints.
* **Nhiệm vụ trong Code:**
    * Khởi tạo cấu trúc dự án backend, cấu hình cấu trúc cấu trúc file (`core/config.py`, `database.py`).
    * Thiết kế hệ thống DB Models (`models.py`) và thực hiện migration.
    * Viết các API endpoints phục vụ cho Auth, Document, và Glossary.
* **Nhiệm vụ viết Báo cáo:**
    * Viết **Lời mở đầu** và **Chương 1** (Khảo sát bài toán, Đặc tả yêu cầu chức năng, Vẽ biểu đồ Use Case).
    * Viết **Chương 2 - Mục 2.1 & 2.2** (Vẽ sơ đồ kiến trúc hệ thống tổng thể, vẽ sơ đồ ERD và đặc tả chi tiết các bảng dữ liệu).
    * Chịu trách nhiệm tổng hợp, căn chỉnh format toàn bộ cuốn báo cáo (Font, Word template, Mục lục).

### 👤 Nguyễn Thế Giáp: AI Agent & Data Engineer
* **Vai trò chính:** Hiện thực hóa luồng xử lý AI, cấu hình LangGraph, tích hợp RAG và tối ưu hóa hệ thống Prompt.
* **Nhiệm vụ trong Code:**
    * Viết module xử lý văn bản `services/doc_processor.py` (Parser PDF/Word, Sentence Splitter).
    * Xây dựng cấu trúc LangGraph trong `agent/graph.py`, viết logic cho các Agent Nodes và cấu hình `agent/tools.py`.
    * Kết nối Vector Database thông qua `services/vector_service.py` để làm RAG cho Glossary/TM.
* **Nhiệm vụ viết Báo cáo:**
    * Viết **Chương 2 - Mục 2.3** (Vẽ sơ đồ khối kiến trúc LangGraph, giải thích cơ chế State Machine và tự sửa lỗi của Agent).
    * Viết **Chương 3 - Mục 3.3** (Giải thích các đoạn code cốt lõi về xử lý file, cấu hình Graph và truy vấn Vector DB).
    * Viết **Chương 4 - Mục 4.2** (Thu thập dữ liệu dịch, lập bảng so sánh kết quả dịch và đánh giá định tính chất lượng đầu ra của AI).

### 👤 Phạm Minh Đức: Frontend Developer & QA (Quality Assurance)
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
