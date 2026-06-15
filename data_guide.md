# HƯỚNG DẪN THU THẬP TÀI LIỆU HỌC THUẬT VÀ XÂY DỰNG GLOSSARY CHUYÊN NGÀNH

Tài liệu này hướng dẫn chi tiết quy trình thu thập dữ liệu nguồn (Dataset) và xây dựng từ điển thuật ngữ chuyên ngành (Glossary) thực tế để nạp vào hệ thống **Smart Trans AI**. Điều này giúp nhóm hoàn thành xuất sắc phần thực nghiệm của bài báo khoa học và chuẩn bị phôi dữ liệu chuẩn cho hệ thống.

---

## 1. Hướng dẫn tìm và thu thập tài liệu học thuật (Dataset)

Đối với một đề tài nghiên cứu khoa học về dịch thuật, chất lượng dữ liệu đầu vào quyết định tính đúng đắn của kết quả thực nghiệm. Nhóm cần thu thập các văn bản tiếng Anh học thuật có độ phức tạp cao về ngữ nghĩa và thuật ngữ.

### 1.1. Các nguồn tài nguyên uy tín
*   **arXiv.org:** Kho lưu trữ mở các bài báo khoa học thuộc các ngành Khoa học Máy tính, Trí tuệ Nhân tạo, Hệ thống Thông tin. Các bài viết ở đây rất mới và chứa nhiều thuật ngữ hiện đại chưa được dịch chuẩn hóa trên Google Translate.
*   **Google Scholar (scholar.google.com):** Công cụ tìm kiếm bài báo khoa học mạnh nhất. Sử dụng các từ khóa chuyên ngành để tìm các bài tổng quan (Survey Paper) - nơi chứa lượng thuật ngữ dày đặc nhất.
*   **Cổng bài giảng Đại học (MIT OpenCourseWare, các trang giáo trình đại học):** Tìm giáo trình tiếng Anh (.pdf) bằng cách sử dụng các toán tử tìm kiếm nâng cao của Google.

### 1.2. Mẹo tìm kiếm tài liệu cụ thể bằng Google Search Operator
Để tìm các chương sách giáo trình hoặc tài liệu bài giảng dạng text học thuật sạch, hãy sử dụng các cú pháp sau:
*   Tìm bài giảng Hệ thống thông tin quản lý dạng PDF:
    `filetype:pdf "management information systems" "lecture notes" OR "chapter"`
*   Tìm tài liệu học máy chuyên sâu:
    `filetype:pdf "machine learning" "introduction" university`
*   Tìm tài liệu về Kiến trúc Agent:
    `filetype:pdf "LLM agent" OR "multi-agent system" survey`

### 1.3. Tiêu chí chọn tài liệu kiểm thử
*   **Độ dài:** Nên chọn một phần tài liệu khoảng **3,000 - 5,000 từ** (tương đương 10 - 15 trang giấy hoặc 1-2 chương giáo trình).
*   **Độ phức tạp:** Văn bản phải chứa các cấu trúc câu phức, câu ghép, nhiều đại từ thay thế (*it, they, this, which*) để kiểm thử hiệu quả của **Context Window** và **Reviewer Agent**.
*   **Định dạng:** Ưu tiên lưu dưới dạng `.txt` (UTF-8) để tránh các lỗi định dạng ký tự lạ khi trích xuất hoặc định dạng `.docx` chuẩn.

---

## 2. Hướng dẫn xây dựng Glossary (Từ điển thuật ngữ) thực tế

Glossary là linh hồn giúp hệ thống duy trì sự đồng bộ và nhất quán thuật ngữ. Việc xây dựng Glossary gồm hai bước: Trích xuất thuật ngữ gốc và Dịch thuật ngữ chuẩn hóa.

### 2.1. Cách trích xuất thuật ngữ gốc tiếng Anh (Source Terms)
Nhóm có thể kết hợp hai cách dưới đây:

#### Cách 1: Sử dụng chính LLM để trích xuất nhanh (Độ chính xác ~90%)
Nạp một phần văn bản nguồn tiếng Anh vào LLM (ví dụ ChatGPT, Gemini) với prompt chuyên biệt sau để bắt lọc từ khóa:
> *"Hãy đọc đoạn văn bản học thuật dưới đây và trích xuất ra toàn bộ các danh từ ghép, thuật ngữ chuyên ngành kỹ thuật/hệ thống thông tin quan trọng xuất hiện trong văn bản. Loại bỏ các từ vựng tiếng Anh giao tiếp thông thường. Xuất kết quả dưới dạng danh sách các từ tiếng Anh đơn lẻ/từ ghép, sắp xếp theo thứ tự chữ cái."*

#### Cách 2: Trích xuất tự động bằng Python (sử dụng thư viện NLTK/SpaCy)
Viết một đoạn script Python ngắn để bóc tách các cụm danh từ (Noun Phrases) có tần suất xuất hiện cao trong tài liệu:
```python
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")
with open("input_academic.txt", "r", encoding="utf-8") as f:
    text = f.read()

doc = nlp(text)
# Lọc các cụm danh từ có độ dài từ 2 đến 4 từ
noun_phrases = [chunk.text.strip().lower() for chunk in doc.noun_chunks 
                if len(chunk.text.split()) >= 2 and len(chunk.text.split()) <= 4]

# Đếm tần suất xuất hiện
most_common_terms = Counter(noun_phrases).most_common(50)
for term, count in most_common_terms:
    print(f"{term}: {count}")
```

### 2.2. Dịch thuật ngữ sang tiếng Việt chuẩn hóa
Sau khi có danh sách các từ tiếng Anh, Sinh viên A (Nguyễn Đình Dũng) có trách nhiệm dịch và chuẩn hóa các thuật ngữ này sang tiếng Việt. Để đảm bảo tính học thuật:
*   **Tham khảo giáo trình chính thống:** Sử dụng bản dịch thuật ngữ từ các giáo trình của PTIT, Đại học Bách Khoa, hoặc sách xuất bản chính thức.
*   **Tính nhất quán:** Tránh các từ dịch thô. Ví dụ:
    *   *Backpropagation* $\rightarrow$ *Lan truyền ngược* (không dịch là *truyền bá ngược*).
    *   *Gradient Descent* $\rightarrow$ *Cực tiểu hóa gradient* hoặc *Thuật toán xuống dốc* (nhất quán chọn 1 cách).
    *   *Overfitting* $\rightarrow$ *Quá khớp* (không dịch là *học quá mức*).

### 2.3. Định dạng Glossary nạp vào cơ sở dữ liệu
Hệ thống **Smart Trans AI** chấp nhận nạp Glossary qua API hoặc tạo trực tiếp bằng file JSON. Định dạng JSON chuẩn bắt buộc phải tuân theo cấu trúc sau:
```json
[
  {
    "source_term": "Machine Learning",
    "target_term": "Học máy",
    "notes": "Lĩnh vực nghiên cứu thuật toán tự học từ dữ liệu"
  },
  {
    "source_term": "Overfitting",
    "target_term": "Quá khớp",
    "notes": "Hiện tượng mô hình khớp quá mức với dữ liệu huấn luyện và mất đi tính tổng quát"
  },
  {
    "source_term": "Context Window",
    "target_term": "Cửa sổ ngữ cảnh",
    "notes": "Đoạn văn bản bao quanh câu đích để cung cấp thêm thông tin cho LLM"
  }
]
```
*Lưu ý:* Lưu file với tên `glossary.json` (sử dụng bảng mã UTF-8) để tránh bị lỗi hiển thị tiếng Việt có dấu.

---

## 3. Quy trình làm sạch dữ liệu học thuật (Data Cleaning)

Văn bản học thuật khi tải xuống từ internet thường chứa nhiều "rác" định dạng. Nhóm cần tiến hành làm sạch trước khi đưa vào hệ thống dịch:

1.  **Loại bỏ Header và Footer:** Xóa sạch các thông tin dòng đầu trang, cuối trang, tên tác giả, tên tạp chí, số trang xuất hiện lặp đi lặp lại ở đầu/cuối mỗi trang.
2.  **Loại bỏ chú thích tài liệu tham khảo:** Các ký tự dạng `[1]`, `[2, 3]`, hoặc `(Vaswani et al., 2017)` nên được dọn dẹp sạch sẽ để tránh làm rối bộ chia câu và gây lỗi dịch thuật cho LLM.
3.  **Xử lý ngắt dòng lỗi:** File PDF thường tự động ngắt dòng bằng dấu gạch ngang (`-`) ở cuối dòng khi từ bị xuống dòng (ví dụ: *hyper-parameter* ngắt thành *hyper-* và *parameter* ở dòng dưới). Cần nối lại các từ này trước khi dịch.
4.  **Chuẩn hóa khoảng trắng:** Loại bỏ các dòng trống thừa thãi, đảm bảo các câu kết thúc bằng dấu chấm và cách nhau bởi đúng một khoảng trắng. điều này giúp công cụ chia câu bằng Regex hoặc NLTK hoạt động chính xác 100%.
