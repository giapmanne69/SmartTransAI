# TÀI LIỆU KỸ THUẬT PHÁT TRIỂN CORE ENGINE SMART TRANS AI

**Phụ trách:** Nguyễn Thế Giáp – Nhóm trưởng

**Vai trò:** AI Agent Engineer & Data Engineer

**Phạm vi báo cáo:** Chương 3 – Phương pháp nghiên cứu và thiết kế hệ thống

**Môi trường triển khai:** Python 3.10+, Jupyter Notebook hoặc Google Colab

---

# 1. Mục tiêu xây dựng Core Engine

## 1.1. Bài toán đặt ra

Trong các hệ thống dịch thuật truyền thống hoặc khi sử dụng các mô hình ngôn ngữ lớn (LLM) theo cơ chế Zero-shot, quá trình dịch thuật học thuật thường gặp ba vấn đề chính:

* Sai lệch thuật ngữ chuyên ngành (Terminology Hallucination).
* Thiếu tính nhất quán giữa các phần của tài liệu dài.
* Không tận dụng được ngữ cảnh liên kết giữa các câu.

Các hạn chế này đặc biệt nghiêm trọng đối với tài liệu khoa học, nghiên cứu và giáo trình chuyên ngành.

## 1.2. Mục tiêu của Core Engine

Core Engine được thiết kế nhằm giải quyết các vấn đề trên thông qua ba cơ chế cốt lõi:

### (1) Vòng lặp tự hiệu chỉnh (Self-Correction Loop)

Thay vì sinh bản dịch duy nhất, hệ thống sử dụng hai Agent:

* Translator Agent
* Reviewer Agent

Hai Agent phối hợp trong một đồ thị trạng thái (State Graph) để phát hiện và sửa lỗi ngữ nghĩa trước khi xuất kết quả cuối cùng.

### (2) Chuẩn hóa thuật ngữ học thuật

Hệ thống tích hợp cơ chế Retrieval-Augmented Generation (RAG) cục bộ nhằm:

* Truy xuất thuật ngữ liên quan.
* Ép buộc mô hình tuân thủ từ điển chuyên ngành.
* Tăng tính nhất quán của bản dịch.

### (3) Bảo toàn ngữ cảnh liên tục

Thay vì dịch từng câu riêng lẻ, hệ thống sử dụng cửa sổ ngữ cảnh (Context Window) bao gồm:

* Câu trước.
* Câu hiện tại.
* Câu sau.

Nhờ đó mô hình có thể hiểu được:

* Đại từ thay thế.
* Liên kết logic.
* Quan hệ nhân quả giữa các câu.

---

# 2. Cấu trúc mã nguồn Core Engine

```text
smart-trans-kernel/
│
├── data/
│   ├── input_academic.txt
│   ├── glossary.json
│   └── output_agent_translation.txt
│
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── document_processor.py
│
├── agent/
│   ├── __init__.py
│   ├── graph.py
│   ├── prompts.py
│   └── tools.py
│
├── main_experimental.ipynb
│
└── requirements.txt
```

Trong đó:

| Thành phần              | Chức năng                     |
| ----------------------- | ----------------------------- |
| data                    | Lưu dữ liệu đầu vào và đầu ra |
| document_processor.py   | Tiền xử lý văn bản            |
| tools.py                | Truy xuất thuật ngữ           |
| prompts.py              | Định nghĩa Prompt cho Agent   |
| graph.py                | Thiết kế LangGraph Workflow   |
| main_experimental.ipynb | Chạy toàn bộ Pipeline         |

---

# 3. Quy trình triển khai hệ thống

## 3.1. Bước 1 – Tiền xử lý tài liệu

### Mục tiêu

Phân tách tài liệu thành các đơn vị dịch nhưng vẫn bảo toàn ngữ cảnh.

### Nhiệm vụ

* Đọc dữ liệu từ file `input_academic.txt`.
* Tách câu bằng NLTK hoặc Regex.
* Tạo Context Window cho mỗi câu.

### Cấu trúc dữ liệu

```python
chunk = {
    "chunk_id": int,
    "origin_text": str,
    "context_window": str
}
```

### Ví dụ

```python
chunk = {
    "chunk_id": 5,
    "origin_text": "It significantly improves performance.",
    "context_window":
    "The neural network was trained on a large dataset. "
    "It significantly improves performance. "
    "The results are reported in Table 2."
}
```

### Kết quả đầu ra

Danh sách các Chunk có ngữ cảnh đầy đủ để đưa vào Agent.

---

## 3.2. Bước 2 – Truy xuất thuật ngữ chuyên ngành

### Mục tiêu

Tự động phát hiện các thuật ngữ học thuật xuất hiện trong câu nguồn.

### Dữ liệu đầu vào

```json
[
  {
    "source": "Machine Learning",
    "target": "Học máy"
  }
]
```

### Quy trình

#### Bước 1

Đọc Glossary từ file JSON.

#### Bước 2

Biểu diễn văn bản bằng:

* TF-IDF
* Embedding

#### Bước 3

Tính độ tương đồng Cosine.

### Công thức

[
Similarity(Q,V)=\frac{Q \cdot V}{||Q|| \times ||V||}
]

Trong đó:

* Q là vector của câu hiện tại.
* V là vector của thuật ngữ trong từ điển.

### Kết quả đầu ra

```python
[
  {
    "source": "Machine Learning",
    "target": "Học máy"
  }
]
```

---

## 3.3. Bước 3 – Thiết kế Agent Workflow

Đây là phần trọng tâm của Chương 3.

### 3.3.1. Translator Agent

Nhiệm vụ:

* Dịch văn bản.
* Sử dụng Context Window.
* Tuân thủ Glossary.

Đầu vào:

```python
{
    "origin_text": "...",
    "context_window": "...",
    "glossary_found": [...]
}
```

Đầu ra:

```python
{
    "raw_translation": "..."
}
```

---

### 3.3.2. Reviewer Agent

Nhiệm vụ:

* Kiểm tra lỗi thuật ngữ.
* Kiểm tra lỗi ngữ nghĩa.
* Đánh giá mức độ học thuật.

Đầu ra bắt buộc ở dạng JSON:

```json
{
  "has_error": true,
  "error_type": "Terminology Mismatch",
  "feedback": "Thuật ngữ Machine Learning phải được dịch là Học máy",
  "is_valid": false
}
```

---

### 3.3.3. Thiết kế AgentState

```python
class AgentState(TypedDict):
    origin_text: str
    glossary_found: list
    raw_translation: str
    review_feedback: str
    loop_count: int
```

---

### 3.3.4. Thiết kế State Graph

```text
START
  │
  ▼
Translator
  │
  ▼
Reviewer
  │
  ├── is_valid = False
  │        │
  │        ▼
  └── Translator
           │
           ▼
       Reviewer
           │
           ▼
          END
```

### Luật điều hướng

Nếu:

```python
is_valid == False
and
loop_count < 3
```

thì:

```text
Reviewer → Translator
```

Ngược lại:

```text
Reviewer → END
```

---

## 3.4. Bước 4 – Vận hành Pipeline

### Quy trình

```text
Input Document
      │
      ▼
Document Processor
      │
      ▼
Glossary Retrieval
      │
      ▼
Translator Agent
      │
      ▼
Reviewer Agent
      │
      ▼
Final Translation
      │
      ▼
Output File
```

### Kết quả đầu ra

```text
data/output_agent_translation.txt
```

Tệp này chứa toàn bộ bản dịch đã được hiệu chỉnh bởi Agent Workflow.

---

# 4. Kịch bản kiểm thử Core Engine

## 4.1. Kịch bản 1 – Độ chính xác truy xuất thuật ngữ

### Mục tiêu

Đánh giá khả năng phát hiện thuật ngữ chuyên ngành.

### Dữ liệu kiểm thử

Ví dụ:

```text
Neural Networks
Deeply Learned Features
Machine Learning Algorithms
```

### Kết quả mong đợi

Hệ thống truy xuất đúng thuật ngữ gốc trong Glossary.

### Chỉ số

```text
Glossary Retrieval Accuracy (%)
```

---

## 4.2. Kịch bản 2 – Kiểm thử vòng lặp tự sửa lỗi

### Mục tiêu

Kiểm tra cơ chế phản hồi giữa Translator và Reviewer.

### Luồng mong đợi

```text
Vòng 1:
Translator
    ↓
Reviewer
    ↓
Phát hiện lỗi

Vòng 2:
Translator nhận Feedback
    ↓
Dịch lại
    ↓
Reviewer
    ↓
Chấp nhận
```

### Minh chứng

* Log LangGraph.
* Log Terminal.
* JSON phản hồi của Reviewer.

---

## 4.3. Kịch bản 3 – Đánh giá hiệu quả Context Window

### Mục tiêu

Đánh giá khả năng xử lý đại từ mơ hồ.

### Nhóm A

Không sử dụng Context Window.

```text
It improves performance.
```

### Nhóm B

Sử dụng Context Window.

```text
The proposed neural network was trained on a large dataset.
It improves performance.
```

### Kết quả mong đợi

Nhóm B dịch chính xác thực thể được đại diện bởi từ “It”, trong khi Nhóm A dễ sinh lỗi ngữ nghĩa.

---

# 5. Kết quả mong đợi

Sau khi hoàn thành toàn bộ Pipeline, hệ thống phải đạt được các mục tiêu:

* Dịch thuật có kiểm soát bằng Agent Workflow.
* Tự động chuẩn hóa thuật ngữ chuyên ngành.
* Giảm lỗi ngữ nghĩa thông qua vòng lặp phản biện.
* Duy trì ngữ cảnh liên tục bằng Context Window.
* Sinh dữ liệu đầu ra phục vụ đánh giá và nghiên cứu mở rộng trong tương lai.

Tài liệu này đồng thời là cơ sở kỹ thuật để xây dựng Chương 3 (Phương pháp nghiên cứu) và Chương 4 (Đánh giá giải pháp) của báo cáo Smart Trans AI.
