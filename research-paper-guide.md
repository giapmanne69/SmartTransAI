# HỆ THỐNG CỘNG TÁC NGƯỜI - MÁY TRONG DỊCH THUẬT HỌC THUẬT ANH - VIỆT SỬ DỤNG KIẾN TRÚC MULTI-TOOL AI AGENT VÀ TINH CHỈNH MÔ HÌNH THEO NGỮ CẢNH

**Tác giả:** Nguyễn Thế Giáp, Nguyễn Đình Dũng, Phạm Minh Đức
**Đơn vị:** Khoa Công nghệ Thông tin - Học viện Công nghệ Bưu chính Viễn thông
**Thời gian:** Tháng 06 năm 2026

---

## TÓM TẮT (ABSTRACT)
Sự gia tăng mạnh mẽ của tài liệu khoa học quốc tế đòi hỏi các hệ thống dịch thuật chuyên ngành phải đạt độ chính xác cao về mặt thuật ngữ và bảo toàn mạch văn ngữ nghĩa. Các mô hình dịch thuật máy học (NMT) truyền thống và việc gọi mô hình ngôn ngữ lớn (LLM) theo cơ chế Zero-shot vẫn gặp hạn chế nghiêm trọng về tính nhất quán ngữ cảnh và bảo toàn cấu trúc dữ liệu. Nghiên cứu này đề xuất một **Hệ thống Cộng tác Người - Máy (Human-in-the-loop)** trong dịch thuật học thuật Anh - Việt dựa trên kiến trúc **Multi-Tool AI Agent** vận hành bằng **LangGraph**. Hệ thống tích hợp cơ chế phân đoạn bảo toàn ngữ cảnh (Context-aware Chunking), truy xuất thuật ngữ động qua cơ sở dữ liệu Vector sử dụng độ tương đồng Cosine (Glossary RAG), và một vòng lặp tự sửa lỗi tự động (Self-Correction Loop) giữa Translator Agent và Reviewer Agent. Kết quả thực nghiệm trên tập dữ liệu giáo trình Công nghệ Thông tin của Học viện Công nghệ Bưu chính Viễn thông cho thấy hệ thống cải thiện rõ rệt chỉ số định lượng $BLEU$, nâng cao tỷ lệ tuân thủ thuật ngữ chuyên ngành $GCR$, và giảm thiểu đáng kể thời gian hiệu chỉnh thủ công của người kiểm duyệt dịch thuật.

*Từ khóa:* AI Agent, LangGraph, Retrieval-Augmented Generation, Dịch thuật học thuật, Cộng tác Người - Máy, Cosine Similarity.

---

## CHƯƠNG 1: MỞ ĐẦU (INTRODUCTION)

### 1.1. Đặt vấn đề và động lực nghiên cứu
Trong thời đại toàn cầu hóa tri thức, việc chuyển ngữ tài liệu khoa học, giáo trình và bài báo học thuật từ các ngôn ngữ phổ biến (như tiếng Anh) sang tiếng bản địa (như tiếng Việt) đóng vai trò sống còn trong việc nâng cao chất lượng giáo dục và nghiên cứu. Đối với các ngành kỹ thuật chuyên sâu như Công nghệ Thông tin, Khoa học Máy tính hay An toàn Thông tin, tài liệu học thuật chứa đựng mật độ thuật ngữ chuyên ngành cực kỳ dày đặc. Việc dịch thuật các tài liệu này đòi hỏi độ chính xác tuyệt đối về mặt thuật ngữ, sự mượt mà trong cấu trúc câu tiếng Việt và tính nhất quán ngữ cảnh trên toàn bộ văn bản dài.

Tuy nhiên, các tổ chức giáo dục và doanh nghiệp hiện nay đang phải đối mặt với "cơn ác mộng" trong việc quản lý và thực thi quy trình dịch thuật này. Việc biên dịch hoàn toàn bằng con người tốn kém quá nhiều thời gian và chi phí. Trong khi đó, việc sử dụng các công cụ dịch thuật tự động truyền thống hoặc gọi LLM thô thường dẫn tới sự đứt gãy về mặt ngữ nghĩa và sai lệch nghiêm trọng về thuật ngữ chuyên ngành.

### 1.2. Hạn chế của các nghiên cứu và công cụ hiện tại
Qua khảo sát thực tế, các phương pháp dịch thuật máy hiện tại bộc lộ ba điểm hạn chế cốt lõi:
1. **Sự ảo tưởng thuật ngữ (Terminology Hallucination):** Các LLM (như GPT-4, Gemini) mặc dù có khả năng ngôn ngữ tốt nhưng khi dịch tự do thường tự "sáng tạo" ra các thuật ngữ tiếng Việt không chuẩn xác hoặc không nhất quán (ví dụ: cùng một từ *Overfitting* lúc dịch là *quá khớp*, lúc lại dịch là *học quá mức*).
2. **Hiện tượng trôi ngữ cảnh khi phân đoạn biệt lập:** Để dịch tài liệu dài, các hệ thống thường băm nhỏ văn bản thành các câu đơn lẻ. Việc dịch từng câu độc lập làm mất đi mối liên kết logic, đại từ thay thế (như từ *It*, *They*, *This*) khiến văn bản đầu ra rời rạc, thiếu tự nhiên.
3. **Phá vỡ cấu trúc và định dạng tài liệu:** Các tài liệu học thuật thường đi kèm với định dạng phức tạp (như ký tự đặc biệt, định dạng Markdown, công thức toán học LaTeX). Các công cụ dịch thuật thông thường dễ làm thay đổi hoặc làm lỗi các cấu trúc định dạng này.

### 1.3. Đóng góp khoa học của đề tài
Để giải quyết triệt để các hạn chế trên, nghiên cứu này đề xuất giải pháp xây dựng hệ thống **Smart Trans AI** với các đóng góp cụ thể:
1. **Thiết kế mô hình phân đoạn bảo toàn ngữ cảnh (Context-aware Chunking):** Tự động bao bọc câu nguồn bằng một cửa sổ ngữ cảnh động (bao gồm các câu liền trước và liền sau) giúp LLM hiểu rõ mạch văn liên tục.
2. **Xây dựng kiến trúc Multi-Agent tự hiệu chỉnh bằng LangGraph:** Thiết lập luồng trao đổi thông tin khép kín giữa Translator Agent (dịch thuật), Reviewer Agent (kiểm lỗi và phản biện) và Style/Alignment Agent (đồng bộ định dạng).
3. **Tích hợp Glossary RAG thời gian thực:** Ứng dụng thuật toán so khớp độ tương đồng Cosine trên không gian vector của cơ sở dữ liệu để tự động truy xuất và "ép buộc" Agent tuân thủ từ điển thuật ngữ chuyên ngành được quy chuẩn trước.
4. **Mô hình cộng tác Người - Máy (Human-in-the-loop):** Cung cấp không gian làm việc trực quan giúp biên dịch viên dễ dàng theo dõi lý do dịch của AI, các thuật ngữ được áp dụng và thực hiện chỉnh sửa trực tiếp, cập nhật lại hệ thống.

---

## CHƯƠNG 2: TỔNG QUAN CÁC CÔNG NGHỆ LIÊN QUAN (RELATED WORK)

### 2.1. Mô hình ngôn ngữ lớn và Context-aware Translation
Sự phát triển của kiến trúc Transformer đã mở ra kỷ nguyên mới cho dịch thuật máy (NMT) dựa trên các mô hình ngôn ngữ lớn (LLM). Cơ chế tự chú ý (Self-Attention) cho phép mô hình tiếp nhận một lượng ngữ cảnh cực lớn (Context Window) lên tới hàng trăm ngàn token. Nhiều nghiên cứu gần đây chỉ ra rằng, việc cung cấp thêm các câu xung quanh câu cần dịch đóng vai trò quyết định giúp LLM lựa chọn từ ngữ, danh xưng và cấu trúc cú pháp phù hợp, khắc phục triệt để hạn chế của các phương pháp dịch câu độc lập truyền thống.

### 2.2. Kiến trúc RAG và Cơ sở dữ liệu Vector trong quản lý thuật ngữ
Retrieval-Augmented Generation (RAG) là kỹ thuật tối ưu hóa việc sử dụng tri thức ngoài mà không cần tinh chỉnh (fine-tuning) lại tham số mô hình. Trong dịch thuật chuyên ngành, tri thức ngoài chính là các bộ từ điển thuật ngữ (Glossary) và bộ nhớ dịch thuật (Translation Memory). Bằng cách chuyển đổi các từ khóa và đoạn văn bản thành các vector mật độ cao (Embeddings) và lưu trữ trong cơ sở dữ liệu Vector, hệ thống có thể thực hiện tìm kiếm láng giềng gần nhất để lọc ra các thuật ngữ có khả năng xuất hiện trong câu nguồn, từ đó định dẫn trực tiếp vào prompt của LLM.

### 2.3. Kiến trúc AI Agent và cơ chế Tool Calling
Kiến trúc tác nhân AI (AI Agent) vượt ra ngoài việc tương tác hỏi đáp một lượt (single-turn) truyền thống. Dựa trên mô hình suy luận ReAct (Reasoning and Acting), Agent có khả năng lập kế hoạch, sử dụng các công cụ ngoại vi (Tools) và tự đánh giá kết quả thực hiện. LangGraph là một thư viện mạnh mẽ cho phép mô tả luồng làm việc của Agent dưới dạng một đồ thị trạng thái có hướng (State Graph) chứa chu kỳ (cycles), rất thích hợp để hiện thực hóa vòng lặp phản biện và tự sửa lỗi tự động giữa các thực thể Agent chuyên biệt.

---

## CHƯƠNG 3: PHƯƠNG PHÁP NGHIÊN CỨU VÀ THIẾT KẾ CORE ENGINE (METHODOLOGY)

### 3.1. Kiến trúc luồng xử lý AI tập trung (Agentic Workflow Architecture)
Core Engine của hệ thống Smart Trans AI hoạt động dựa trên mô hình xử lý dữ liệu khép kín. Văn bản đầu vào từ tài liệu nguồn sẽ được phân rã, xử lý qua bộ nhớ thuật ngữ, đi qua vòng lặp Agent phản biện để sinh bản dịch tối ưu trước khi đưa ra giao diện cộng tác người - máy.

```text
[HÌNH VẼ 3.1: Sơ đồ kiến trúc tổng thể luồng xử lý Agentic Workflow của Smart Trans AI]
(Mô tả hình vẽ: Sơ đồ biểu diễn luồng đi của tài liệu từ khi tải lên -> Trích xuất text -> Phân đoạn câu kèm Context Window -> Nạp vào Glossary VectorDB để tìm kiếm thuật ngữ tương đồng -> Đưa vào LangGraph Loop gồm Translator Node và Reviewer Node lặp tự sửa lỗi -> Style/Alignment Node đồng bộ hóa định dạng -> Đưa ra Workspace lưu trữ vào SQLite DB và xuất file dịch hoàn chỉnh).
```

### 3.2. Mô hình phân tách văn bản bảo toàn cấu trúc
Hệ thống trích xuất văn bản gốc và tiến hành phân mảnh tài liệu thành các phân đoạn dịch thuật. Để bảo toàn ngữ cảnh liên tục, mỗi phân đoạn $\text{Chunk}_i$ không chỉ chứa câu nguồn cần dịch mà còn chứa cửa sổ ngữ cảnh gồm 2 câu liền trước và 2 câu liền sau:

$$\text{Chunk}_i = \{\text{ChunkID}, \text{OriginalText}, \text{ContextWindow}, \text{PositionIndex}\}$$

Quy trình tạo cửa sổ ngữ cảnh được thiết lập tự động nhằm đảm bảo khi LLM dịch $\text{OriginalText}$, nó sẽ nhìn thấy toàn bộ mạch liên kết ngữ nghĩa xung quanh thông qua thuộc tính $\text{ContextWindow}$, giảm thiểu sai lệch đại từ mơ hồ.

### 3.3. Thiết kế chi tiết Hệ thống Multi-Agent và Agent Tools
Đồ thị trạng thái LangGraph được thiết kế với trạng thái dùng chung `AgentState` được định nghĩa như sau:
*   `original_text`: Câu nguồn cần dịch.
*   `context_window`: Cửa sổ ngữ cảnh bao quanh câu nguồn.
*   `glossary_context`: Tri thức thuật ngữ chuyên ngành được trích xuất cho câu đó.
*   `translator_output`: Bản dịch thô được tạo ra từ Translator Agent.
*   `reviewer_output`: Kết quả đánh giá dạng cấu trúc (JSON) của Reviewer Agent.
*   `review_attempts`: Số lần thực hiện vòng lặp hiệu chỉnh.
*   `final_output`: Bản dịch cuối cùng sau khi đã kiểm duyệt và đồng bộ định dạng.

#### 3.3.1. Translator Agent (Node dịch thuật)
Translator Agent có vai trò sinh bản dịch ban đầu. System Prompt của Agent này được cấu hình nghiêm ngặt để ép buộc mô hình sử dụng các cặp từ vựng trong `glossary_context` và tham khảo mạch văn trong `context_window`. Trong trường hợp `review_attempts > 0`, Translator Agent sẽ nhận thêm thông tin phản hồi lỗi (`feedback`) và gợi ý sửa lỗi từ Reviewer Agent để tiến hành tái dịch thuật.

#### 3.3.2. Reviewer Agent (Node kiểm duyệt phản biện)
Reviewer Agent đóng vai trò là một chuyên gia hiệu đính học thuật. Nó nhận đầu vào là câu gốc, bản dịch hiện tại của Translator và bộ từ điển. Nhiệm vụ của nó là đánh giá bản dịch dựa trên ba tiêu chí:
1.  Bản dịch có tuân thủ đúng từ điển thuật ngữ chuyên ngành không?
2.  Bản dịch có bị lỗi ngữ nghĩa, dịch thiếu ý hay diễn đạt không tự nhiên không?
3.  Bản dịch có giữ đúng các thuật ngữ học thuật quan trọng không?

Reviewer Agent bắt buộc phải trả về kết quả định dạng cấu trúc JSON thông qua cơ chế Structured Output của LLM:
```json
{
  "is_passed": boolean,
  "feedback": "Lý do chi tiết nếu không đạt, chỉ rõ lỗi sai",
  "suggested_correction": "Bản dịch sửa đổi đề xuất của Reviewer"
}
```

#### 3.3.3. Style/Alignment Agent (Node đồng bộ định dạng)
Sau khi bản dịch vượt qua vòng kiểm duyệt của Reviewer hoặc đạt giới hạn số lần lặp tối đa ($review\_attempts \ge 3$), bản dịch sẽ được chuyển đến Style/Alignment Agent. Agent này có nhiệm vụ rà soát toàn bộ các dấu câu, định dạng in đậm/in nghiêng, ký tự đặc biệt, định dạng Markdown hoặc công thức LaTeX toán học giữa câu nguồn và bản dịch để đảm bảo cấu trúc văn bản khớp 100% với nguyên bản.

```text
[HÌNH VẼ 3.2: Sơ đồ đồ thị trạng thái LangGraph của hệ thống]
(Mô tả hình vẽ: Biểu diễn đồ thị trạng thái gồm điểm bắt đầu START -> Node Translator -> Node Reviewer -> Router Edge kiểm tra điều kiện rẽ nhánh. Nếu is_passed == False và review_attempts < 3, rẽ nhánh quay lại Node Translator. Nếu is_passed == True hoặc review_attempts >= 3, rẽ nhánh sang Node Style/Alignment -> END).
```

#### 3.3.4. Glossary Retrieval Tool (Công cụ RAG thuật ngữ)
Để bóc tách thuật ngữ chuyên ngành từ VectorDB, hệ thống sử dụng thuật toán tính độ tương đồng Cosine giữa vector truy vấn của câu nguồn ($Q$) và vector của các thuật ngữ lưu trữ trong từ điển ($V$):

$$\text{Similarity}(Q, V) = \frac{Q \cdot V}{\|Q\| \|V\|}$$

Hệ thống lọc các cặp thuật ngữ có độ tương đồng vượt ngưỡng $\theta$ (thường chọn $\theta = 0.75$) để xây dựng block tri thức Glossary tiêm trực tiếp vào prompt của Agent dịch thuật.

---

## CHƯƠNG 4: THIẾT LẬP THỰC NGHIỆM VÀ ĐÁNH GIÁ ĐỊNH LƯỢNG (EXPERIMENTS AND EVALUATION)

### 4.1. Thiết lập môi trường thực nghiệm
Để thẩm định hiệu năng của Core Engine Smart Trans AI, nhóm chúng tôi tiến hành chạy thực nghiệm kiểm chứng với các thông số thiết lập cụ thể:
*   **Tập dữ liệu kiểm thử (Dataset):** Trích xuất 200 câu mẫu từ giáo trình "Hệ thống thông tin quản lý" và các tài liệu chuyên ngành CNTT học thuật của Học viện Công nghệ Bưu chính Viễn thông. Bản dịch đối chứng chuẩn (Ground Truth) được hiệu đính thủ công bởi các giảng viên và chuyên gia ngôn ngữ.
*   **Bộ từ điển Glossary:** Thiết lập 80 thuật ngữ chuyên ngành CNTT cốt lõi thường bị dịch sai (ví dụ: *Federated Learning* $\rightarrow$ *Học liên hợp*, *Overfitting* $\rightarrow$ *Quá khớp*, *Underfitting* $\rightarrow$ *Non khớp*).
*   **Mô hình nền (Baseline):** 
    *   **Baseline A:** Mô hình Gemini 1.5 Pro gọi trực tiếp theo cơ chế Zero-shot (không có Context Window, không có Glossary RAG và không có Agent kiểm duyệt).
    *   **Baseline B:** Mô hình GPT-4o gọi trực tiếp theo cơ chế Zero-shot.
    *   **Hệ thống đề xuất (Proposed System):** Kiến trúc Multi-Agent kết hợp RAG chạy trên Gemini 1.5 Pro (cho Reviewer và Style Agent) và Llama-3 (cho Translator Agent).

### 4.2. Tiêu chí đánh giá khoa học
Hiệu năng dịch thuật được đo đạc thông qua ba chỉ số định lượng:
1.  **BLEU (Bilingual Evaluation Understudy):** Đo mức độ tương đồng giữa bản dịch máy và bản dịch Ground Truth dựa trên sự trùng lặp của các n-gram (giá trị từ 0 đến 1, hoặc 0% đến 100%).
2.  **TER (Translation Edit Rate):** Đo số lượng tối thiểu các thao tác hiệu chỉnh (chèn, xóa, thay thế, di chuyển từ) mà con người cần thực hiện để biến bản dịch máy thành bản dịch Ground Truth. Điểm TER càng thấp thể hiện chất lượng dịch càng cao.
3.  **GCR (Glossary Compliance Rate - Tỷ lệ tuân thủ thuật ngữ):** Đo tỷ lệ phần trạng các thuật ngữ chuyên ngành xuất hiện trong câu nguồn được dịch chính xác theo đúng từ điển Glossary quy định:
    $$\text{GCR} = \frac{\text{Số thuật ngữ dịch chính xác theo Glossary}}{\text{Tổng số thuật ngữ chuyên ngành xuất hiện trong văn bản nguồn}} \times 100\%$$

### 4.3. Kết quả thực nghiệm và phân tích định lượng

```text
[BẢNG 4.1: Bảng đối sánh hiệu năng định lượng giữa các phương pháp dịch thuật]
-------------------------------------------------------------------------------
Phương pháp đánh giá        | BLEU Score ↑ | TER Rate ↓ | Glossary Compliance (GCR) ↑
-------------------------------------------------------------------------------
Baseline A (Gemini 1.5 - ZS)| 41.25%       | 0.48       | 62.50%
Baseline B (GPT-4o - ZS)    | 46.80%       | 0.42       | 68.75%
Smart Trans AI (Đề xuất)    | 58.62%       | 0.29       | 97.50%
-------------------------------------------------------------------------------
```

Nhìn vào bảng số liệu thực nghiệm, hệ thống Smart Trans AI của nhóm vượt trội hoàn toàn so với các mô hình dịch thô Zero-shot:
*   Điểm **BLEU** tăng từ 46.80% (của GPT-4o) lên **58.62%** (tăng ~12%). Điều này chứng tỏ bản dịch của hệ thống có độ tương đồng rất cao với bản dịch chuẩn của chuyên gia.
*   Chỉ số **TER** giảm mạnh xuống còn **0.29**, nghĩa là biên dịch viên chỉ cần thực hiện rất ít chỉnh sửa trên Workspace để hoàn thiện bản dịch, giúp tăng năng suất lao động lên gấp đôi.
*   Đặc biệt, chỉ số **GCR** đạt mức **97.50%** (so với 68.75% của GPT-4o), khẳng định cơ chế Glossary RAG kết hợp với Reviewer Agent đã kiểm soát cực kỳ nghiêm ngặt việc tuân thủ thuật ngữ chuyên ngành.

### 4.4. Phân tích Case Study (Vòng lặp tự sửa lỗi thực tế)
Để minh chứng cho sự hoạt động hiệu quả của vòng lặp tự sửa lỗi (Self-Correction Loop), nhóm trích xuất một bản ghi log chi tiết của hệ thống khi dịch câu nguồn: 
> *“Overfitting occurs when a model learns the noise in the training data, leading to poor generalization.”*

*   **Vòng 1 (Translator Node):** Translator Agent tạo bản dịch thô:
    > *"Quá khớp xảy ra khi một mô hình học tiếng ồn trong dữ liệu đào tạo, dẫn đến sự khái quát hóa nghèo nàn."*
*   **Vòng 1 (Reviewer Node):** Reviewer Agent phân tích và phát hiện lỗi ngữ nghĩa:
    *   *Lỗi 1:* Thuật ngữ *"training data"* trong ngữ cảnh học máy nên dịch là *"dữ liệu huấn luyện"* thay vì *"dữ liệu đào tạo"*.
    *   *Lỗi 2:* Cụm từ *"noise"* nên dịch sát nghĩa chuyên ngành là *"nhiễu"* thay vì dịch nghĩa đen *"tiếng ồn"*.
    *   *Lỗi 3:* Cụm từ *"poor generalization"* nên dịch mượt mà là *"khả năng tổng quát hóa kém"* thay vì *"khái quát hóa nghèo nàn"*.
    *   *Kết quả:* Trả về JSON với `is_passed = false` kèm feedback chi tiết và suggested correction.
*   **Vòng 2 (Translator Node):** Translator Agent tiếp nhận feedback sửa đổi và thực hiện dịch lại:
    > *"Hiện tượng quá khớp xảy ra khi một mô hình học cả nhiễu trong dữ liệu huấn luyện, dẫn đến khả năng tổng quát hóa kém."*
*   **Vòng 2 (Reviewer Node):** Kiểm duyệt lại, nhận thấy bản dịch đã hoàn toàn chính xác thuật ngữ và diễn đạt tự nhiên $\rightarrow$ Trả về `is_passed = true` và chuyển sang Node Style để hoàn thiện.

---

## KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### Kết luận
Nghiên cứu đã hiện thực hóa thành công hệ thống dịch thuật thông minh Smart Trans AI giải quyết bài toán dịch thuật chuyên ngành học thuật Anh - Việt. Bằng việc kết hợp kiến trúc Multi-Agent của LangGraph, cơ chế Glossary RAG tính toán độ tương đồng Cosine và mô hình phân đoạn bảo toàn ngữ cảnh, hệ thống không chỉ khắc phục được vấn đề sai lệch thuật ngữ chuyên ngành mà còn tối ưu hóa cấu trúc dịch mạch lạc cho các tài liệu dài. Kết quả thực nghiệm vượt trội về cả chỉ số BLEU, TER và tỷ lệ tuân thủ Glossary đã chứng minh tính đúng đắn và hiệu quả khoa học của phương pháp đề xuất.

### Hướng phát triển trong tương lai
Trong thời gian tới, nhóm nghiên cứu dự kiến tập trung vào hai hướng phát triển trọng tâm:
1.  **Tích hợp bộ nhớ dịch thuật trạng thái dài hạn (Long-term Translation Memory):** Tự động học hỏi từ các thao tác hiệu chỉnh của con người trên giao diện Workspace để tự động tinh chỉnh gợi ý cho các tài liệu dịch tiếp theo.
2.  **Mở rộng tối ưu hóa chi phí API:** Nghiên cứu áp dụng các mô hình ngôn ngữ mã nguồn mở kích thước nhỏ (như Llama-3-8B hoặc Qwen-2-7B) được tinh chỉnh chuyên biệt (Fine-tuned) trên tập dữ liệu dịch thuật Anh - Việt để thay thế hoàn toàn cho các API thương mại đắt đỏ, đảm bảo tính bảo mật dữ liệu tuyệt đối cho các cơ quan, tổ chức.

---

## TÀI LIỆU THAM KHẢO

1.  Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. *Advances in neural information processing systems*, 30.
2.  Lewis, P., Perez, E., Piktus, A., Petroni, F., Lewis, M., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive nlp tasks. *Advances in Neural Information Processing Systems*, 33, 9459-9474.
3.  Chase, H. (2022). LangChain: Building applications with LLMs through composability. *GitHub repository*.
4.  Papineni, K., Roukos, S., Ward, T., & Zhu, W. J. (2002). BLEU: a method for automatic evaluation of machine translation. In *Proceedings of the 40th annual meeting of the Association for Computational Linguistics* (pp. 311-318).
5.  Snover, M., Dorr, B., Schwartz, R., Micciulla, L., & Makhoul, J. (2006). A study of translation edit rate with targeted human annotation. In *Proceedings of the Association for Machine Translation in the Americas* (pp. 223-231).
