# HUONG DAN HOAN THANH BAO CAO BAI TAP LON CUOI KY

Tai lieu nay cung cap:
- Cau truc chi tiet cho bao cao de tai Smart Trans AI.
- Ke hoach phoi hop cho nhom 3 sinh vien trong 4-6 tuan.
- Phan cong ro rang giua cong viec ky thuat va viet bao cao.

## 1. Thong tin nhom va de tai

### 1.1. Thanh vien
- Nguyen Dinh Dung - B22DCCN131
- Nguyen The Giap (Leader) - B22DCCN251
- Pham Minh Duc - B22DCCN239

### 1.2. Ten de tai
He thong Cong tac Nguoi - May trong Dich thuat Hoc thuat Anh - Viet Su dung Kien truc Multi-Tool AI Agent va Tinh chinh Mo hinh theo Ngu canh

### 1.3. Thong tin bieu mau trang bia
**Sinh vien thuc hien:** [Dien ten nhom/ten sinh vien]  
**Ma so sinh vien:** [Dien MSSV]  
**Giang vien huong dan:** [Dien ten giang vien]  
**Don vi:** [Dien ten Truong/Vien]  
*Ha Noi, Thang 06 Nam 2026*

---

## 2. Khung noi dung bao cao

## TOM TAT (ABSTRACT)

- **Boi canh:** Su gia tang manh me cua tai lieu khoa hoc quoc te doi hoi he thong dich thuat dat do chinh xac cao ve thuat ngu va ngu canh. Cac cong cu NMT truyen thong van gap han che khi xu ly ngu canh hoc thuat sau va thuong lam mat dinh dang tep dau vao.
- **Bai toan nghien cuu:** Giai quyet qua tai cho nguoi kiem duyet dich thuat (Translation Censor), dam bao tinh nhat quan thuat ngu xuyen suot tai lieu dai, va bao toan cau truc DOM/XML cua tep.
- **Giai phap de xuat:** Xay dung he thong dich thuat phan quyen dua tren kien truc Multi-Tool AI Agent, tich hop bo nho ngan han, truy van thuat ngu dong qua VectorDB RAG, va bo phat hien loi ngu nghia chuyen nganh. He thong van hanh theo co che human-in-the-loop va luu vet du lieu hieu chinh de phuc vu fine-tuning LLM dai han.
- **Ket qua ky vong:** Toi uu thoi gian hieu chinh cua chuyen gia, tang tinh nhat quan thuat ngu, va xuat ban tai lieu dau ra giu nguyen dinh dang goc.

---

## CHUONG 1: MO DAU (INTRODUCTION)

### 1.1. Dat van de va dong luc nghien cuu
Trong boi canh hoi nhap va bung no thong tin, nhu cau chuyen ngu tai lieu hoc thuat chuyen nganh (CNTT, Y sinh, Kinh te - Tai chinh) giua tieng Anh va tieng Viet ngay cang cap thiet. Dich thuat hoc thuat doi hoi do chuan xac ngu canh cao, tinh nhat quan thuat ngu mang tinh he thong, va kha nang bao toan cau truc van ban phuc tap (bang bieu, so do, lien ket XML/DOM) cua cac dinh dang PDF, Word, HTML.

### 1.2. Han che cua cac nghien cuu va cong cu hien tai
Cong cu dich pho bien hoac cach goi LLM theo co che zero-shot thuong boc lo:
- **Ao tuong thuat ngu (Hallucination):** Dich tu-doi-tu lam sai nghia khoa hoc.
- **Thieu tinh nhat quan:** Cung mot thuat ngu co the bi dich khac nhau o cac phan khac nhau cua tai lieu dai.
- **Mat cau truc tep:** Trich xuat raw text de dich de pha vo dinh dang hien thi, ton nhieu cong sua thu cong.

### 1.3. Dong gop khoa hoc cua de tai
De tai huong toi 3 dong gop chinh:
1. De xuat mo hinh cong tac 3 thanh phan theo RBAC: **User** $\rightarrow$ **AI Agent** $\rightarrow$ **Translation Censor**.
2. Thiet ke **Censor AI Agent** tich hop short-term memory va tool calling de ho tro phat hien loi thuat ngu.
3. Xay dung **Data Logging Pipeline** luu vet phan hoi con nguoi, tao nen tang du lieu vang cho fine-tuning LLM bang QLoRA.

### 1.4. Bo cuc bao cao
1. **Tom tat (Abstract):** Boi canh, bai toan, giai phap, ket qua, tu khoa.
2. **Chuong 1 - Mo dau:** Ly do chon de tai, muc tieu, pham vi, dong gop.
3. **Chuong 2 - Tong quan cong nghe lien quan:** LLM, RAG, AI Agent, RBAC, related work.
4. **Chuong 3 - Phuong phap nghien cuu va thiet ke he thong:** Kien truc, luong xu ly, thiet ke Agent, du lieu, pipeline huan luyen/tinh chinh.
5. **Chuong 4 - Cai dat, thuc nghiem va danh gia:**
     - 4.1. Kich ban kiem thu he thong (test cases, ket qua pass/fail, tieu chi).
     - 4.2. Danh gia chat luong dich (doi sanh thuat ngu, dinh tinh/dinh luong).
     - 4.3. Minh chung giao dien va quy trinh van hanh (Auth, Dashboard, Workspace, Glossary).
6. **Ket luan va huong phat trien:** Tong ket ket qua, han che, lo trinh mo rong.
7. **Tai lieu tham khao:** Trinh bay theo IEEE hoac APA.
8. **Phu luc:** Hinh minh chung, so do kien truc, Use Case, ERD, prompt mau, bang test case day du.

Luu y chuan hoa: Moi hinh anh, bang so lieu va mo ta ky thuat phai trich xuat tu san pham thuc te cua nhom; khong su dung du lieu gia lap khong co trong ma nguon.

---

## CHUONG 2: TONG QUAN CAC CONG NGHE LIEN QUAN (RELATED WORK)

### 2.1. Mo hinh ngon ngu lon (LLM) va dich thuat ngu canh (Context-aware Translation)
Trinh bay su dich chuyen tu RNN/LSTM sang Transformer. Phan tich cach LLM xu ly context window de dich theo mach van ban thay vi tung cau co lap.

### 2.2. Kien truc RAG (Retrieval-Augmented Generation) va co so du lieu Vector
Mo ta co che text embeddings, nguyen ly truy van do tuong dong ngu nghia tren ChromaDB/Milvus, va vai tro cua dynamic glossary trong chat luong dau ra.

### 2.3. Kien truc AI Agent va co che tool calling
Phan tich tu duy Agent theo ReAct (Reasoning and Acting), co che function calling va vai tro cua cong cu ngoai vi trong xac thuc thong tin truoc khi ra quyet dinh.

### 2.4. Quan ly truy cap theo vai tro (RBAC) va bao mat du lieu
Tong quan co che JWT, middleware phan quyen, va dam bao tinh co lap du lieu giua cac nhom nguoi dung.

---

## CHUONG 3: PHUONG PHAP NGHIEN CUU VA THIET KE HE THONG (METHODOLOGY)

### 3.1. Kien truc tong the he thong (System Architecture)
He thong theo huong dich vu, tach ro tang giao dien phan quyen va tang nghiep vu AI core. Luong RBAC qua middleware:
- **User:** Upload, theo doi tien do, download tep.
- **Translation Censor:** Lam viec tai Censor Workspace, tuong tac AI Agent, sua ban dich tho, phe duyet chunk.
- **Admin:** Quan tri tai khoan, tai nguyen he thong, va co so du lieu tu dien goc.

### 3.2. Mo hinh phan tach van ban bao toan cau truc (Structure-preserving Document Parser)
Module `parser_service.py` phan tich PDF/Word/HTML thanh cau truc DOM/XML, trich xuat text kem metadata:

$$\text{Chunk}_i = \{ \text{TextContent}, \text{StyleMetadata}, \text{PositionIndex} \}$$

Sau khi dich va kiem duyet, module `exporter_service.py` map nguoc noi dung moi vao dung metadata va vi tri ban dau de bao toan dinh dang tep.

### 3.3. Kien truc chi tiet Censor AI Agent
Trong tam cua he thong nam o `agent_core.py`, noi Agent van hanh song hanh voi Censor nguoi.

#### 3.3.1. Co che bo nho ngan han (Short-term Memory)
Agent duy tri state buffer theo tung session tai lieu. Moi chinh sua/phe duyet cua Censor duoc ghi vao bo nho nay de dung lai cho cac chunk tiep theo, qua do tang tinh nhat quan va giam lap loi.

#### 3.3.2. Thiet ke va van hanh cac cong cu (Agent Tools)
Agent kich hoat 2 cong cu cot loi qua function calling:

- **Tool 1 - Glossary Retrieval Tool:** Trich xuat named entities, truy van tuong dong cosine tren VectorDB:

$$\text{Similarity}(Q, V) = \frac{Q \cdot V}{\|Q\| \|V\|}$$

Trong do $Q$ la vector nhung cua doan hien tai, $V$ la vector nhung cua tap thuat ngu trong tu dien. Dau ra la danh sach thuat ngu bat buoc.

- **Tool 2 - Academic Error Detection Tool:** Doi chieu ban dich tho voi glossary chuan de phat hien loi ngu nghia, sai thuat ngu, hoac van phong phi hoc thuat. Dau ra JSON de hien thi tren giao dien:

```json
{
    "has_error": true,
    "error_type": "Terminology Mismatch",
    "wrong_phrase": "Tu dich sai",
    "suggested_phrase": "Tu de xuat chuan",
    "reason": "Ly do khoa hoc/ngu canh chuyen nganh"
}
```

---

## CHUONG 4: CAI DAT, THUC NGHIEM VA DANH GIA (IMPLEMENTATION AND EVALUATION)

### 4.1. Kich ban kiem thu he thong (System Test Scenarios)
Xay dung bo test case cho cac luong: dang nhap, upload tai lieu, khoi tao job dich, kiem duyet trong workspace, cap nhat glossary, xuat file. Moi test case can co:
- Dau vao.
- Cac buoc thuc hien.
- Ket qua ky vong.
- Ket qua thuc te.

### 4.2. Danh gia chat luong dich va tinh nhat quan thuat ngu
Thiet lap bang doi sanh giua:
- Ban dich goc (khong ho tro Agent/RAG).
- Ban dich cua he thong Smart Trans AI.

Tieu chi danh gia:
- Do dung thuat ngu.
- Do mach lac ngu canh.
- Ty le loi duoc Censor phat hien.
- Thoi gian hieu chinh trung binh.

### 4.3. Danh gia giao dien va trai nghiem van hanh
Trinh bay anh chup thuc te cho cac man hinh Auth, Dashboard, Workspace, Glossary va mo ta vai tro tung thanh phan trong quy trinh cong tac User - AI Agent - Translation Censor.

---

## KET LUAN VA HUONG PHAT TRIEN
Tong ket ket qua khoa hoc - ky thuat da dat duoc, cac gioi han hien tai, va de xuat huong phat trien tiep theo: tu dong danh gia chat luong dich, human feedback learning, toi uu chi phi suy luan, da ngon ngu.

## TAI LIEU THAM KHAO
Liet ke theo mot chuan trich dan thong nhat (khuyen nghi IEEE/APA), bao gom bai bao khoa hoc, tai lieu LLM/RAG/LangGraph, framework va cong cu da su dung.

## PHU LUC
Tong hop cac minh chung bo sung: Use Case Diagram, ERD, luu do state machine, prompt mau, bang test case day du, va anh chup he thong theo tung phien ban demo.

---

## 3. Phan cong cong viec theo thanh vien

De hoan thanh khoi luong cong viec trong 4-6 tuan, nhom phan ra nhu sau:

### 3.1. Nguyen Dinh Dung - Project Manager va Backend Lead
- **Vai tro chinh:** Thiet ke kien truc he thong, xay dung backend core, quan ly database va API endpoints.
- **Nhiem vu code:**
    - Khoi tao cau truc du an backend, cau hinh file he thong (`core/config.py`, `database.py`).
    - Thiet ke DB models (`models.py`) va migration.
    - Xay dung API cho Auth, Document, Glossary.
- **Nhiem vu bao cao:**
    - Viet Loi mo dau va Chuong 1 (khao sat bai toan, dac ta yeu cau, Use Case).
    - Viet Chuong 2, muc 2.1 va 2.2 (kien truc tong the, ERD, dac ta bang du lieu).
    - Tong hop va can chinh dinh dang toan bo bao cao.

### 3.2. Nguyen The Giap - AI Agent va Data Engineer
- **Vai tro chinh:** Hien thuc luong AI, cau hinh LangGraph, tich hop RAG, toi uu prompt.
- **Nhiem vu code:**
    - Phat trien `services/doc_processor.py` (parser PDF/Word, sentence splitter).
    - Xay dung graph trong `agent/graph.py`, logic node, va `agent/tools.py`.
    - Ket noi VectorDB trong `services/vector_service.py` cho Glossary/TM.
- **Nhiem vu bao cao:**
    - Viet Chuong 2, muc 2.3 (so do khoi LangGraph, co che state machine, tu sua loi).
    - Viet Chuong 3, muc 3.3 (code cot loi xu ly file, graph, truy van vector).
    - Viet Chuong 4, muc 4.2 (thu thap du lieu, doi sanh ket qua dich, danh gia chat luong AI).

### 3.3. Pham Minh Duc - Frontend Developer va QA
- **Vai tro chinh:** Xay dung UI/UX, ket noi API, va kiem thu he thong.
- **Nhiem vu code:**
    - Khoi tao frontend, cau hinh router, context, axios client.
    - Hien thuc UI cho Auth, Dashboard, Glossary trong `features/`.
    - Tap trung man hinh `features/workspace/` (song ngu theo hang, cot goi y AI, glossary dong).
- **Nhiem vu bao cao:**
    - Viet Chuong 3, muc 3.1 va 3.2 (cong nghe su dung, cay cau truc ma nguon backend/frontend).
    - Viet Chuong 4, muc 4.1 va 4.3 (bang test scenario, anh demo, mo ta tung man hinh).
    - Viet phan Ket luan va Huong phat trien.

---

## 4. Quy trinh phoi hop lam viec nhom (Workflow)

```text
Tuan 1: Thong nhat yeu cau -> Thiet ke DB va so do Agent (SV A + B)
Tuan 2-3: Code Core API (SV A) song song voi code LangGraph + RAG (SV B)
Tuan 3-4: Code UI va ket noi API (SV C)
Tuan 5: Viet bao cao theo cau phan da phan cong
Tuan 6: Ghep phoi, chuan hoa tai lieu, tong duyet demo
```

## 5. Checklist truoc khi nop

- Noi dung bao cao day du theo chuong, khong thieu muc.
- Tat ca hinh anh/bang bieu la minh chung that tu he thong.
- Tai lieu tham khao dung mot chuan trich dan thong nhat.
- Thuat ngu su dung nhat quan giua code, giao dien, va bao cao.
- Da soat loi chinh ta, dinh dang, muc luc, danh muc hinh/bang.
- Da tong duyet demo va doi chieu voi cac test case trong Chuong 4.
