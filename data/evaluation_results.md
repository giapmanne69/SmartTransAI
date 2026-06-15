# BÁO CÁO KẾT QUẢ THỰC NGHIỆM ĐỐI SÁNH DỊCH THUẬT

Hệ thống đã chạy thử nghiệm dịch thuật tự động trên 4 phân đoạn câu học thuật chuyên ngành CNTT.

| Phương pháp đánh giá | BLEU Score ↑ | TER Rate ↓ | Glossary Compliance (GCR) ↑ |
| :--- | :---: | :---: | :---: |
| Smart Trans AI (Proposed Agentic + RAG) | 0.00% | 1.00 | 0.00% (0/4) |
| Baseline A (Gemini 1.5 Pro Zero-Shot) | 0.00% | 1.00 | 0.00% (0/4) |
| Baseline B (GPT-4o Mini Zero-Shot) | 0.00% | 1.00 | 0.00% (0/4) |

## CHI TIẾT BẢN DỊCH TỪNG PHÂN ĐOẠN CÂU

### Câu 1:
- **Original (English):** *"An AI Agent performs actions based on context."*
- **Ground Truth (Human):** *"Một Tác nhân AI thực hiện các hành động dựa trên ngữ cảnh."*
- **Smart Trans AI (Proposed Agentic + RAG):** "[Translation Failed]"
  *Phản hồi Reviewer:* Translation failed: Request timed out.
- **Baseline A (Gemini 1.5 Pro Zero-Shot):** "[Translation Failed]"
- **Baseline B (GPT-4o Mini Zero-Shot):** "[Translation Failed]"

### Câu 2:
- **Original (English):** *"The Context Window determines what text is visible to the model."*
- **Ground Truth (Human):** *"Cửa sổ ngữ cảnh quyết định đoạn văn bản nào mô hình có thể nhìn thấy."*
- **Smart Trans AI (Proposed Agentic + RAG):** "[Translation Failed]"
  *Phản hồi Reviewer:* Translation failed: Request timed out.
- **Baseline A (Gemini 1.5 Pro Zero-Shot):** "[Translation Failed]"
- **Baseline B (GPT-4o Mini Zero-Shot):** "[Translation Failed]"

### Câu 3:
- **Original (English):** *"Overfitting occurs when a model learns the noise in the training data."*
- **Ground Truth (Human):** *"Hiện tượng quá khớp xảy ra khi một mô hình học nhiễu trong dữ liệu huấn luyện."*
- **Smart Trans AI (Proposed Agentic + RAG):** "[Translation Failed]"
  *Phản hồi Reviewer:* Translation failed: Request timed out.
- **Baseline A (Gemini 1.5 Pro Zero-Shot):** "[Translation Failed]"
- **Baseline B (GPT-4o Mini Zero-Shot):** "[Translation Failed]"

### Câu 4:
- **Original (English):** *"This machine learning algorithm achieves high accuracy on the test set."*
- **Ground Truth (Human):** *"Thuật toán học máy này đạt được độ chính xác cao trên tập kiểm thử."*
- **Smart Trans AI (Proposed Agentic + RAG):** "[Translation Failed]"
  *Phản hồi Reviewer:* Translation failed: Request timed out.
- **Baseline A (Gemini 1.5 Pro Zero-Shot):** "[Translation Failed]"
- **Baseline B (GPT-4o Mini Zero-Shot):** "[Translation Failed]"
