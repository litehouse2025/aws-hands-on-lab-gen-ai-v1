## Tổng quan tài liệu

Tài liệu này giải thích các khái niệm **Parsing** và **Chunking** - hai kỹ thuật quan trọng khi xây dựng Knowledge Base cho AI Agent.

---

## Phần 1: Parsing

### **Parsing Là Gì?**

**Định nghĩa:**
```
Parsing = Quá trình đọc và trích xuất thông tin từ file
• Hiểu được format của file
• Tách các phần khác nhau
• Chuyển đổi thành định dạng có cấu trúc
```

**Ví Dụ:**
```
File gốc (CSV):
name,age,email
John,30,john@example.com
Jane,25,jane@example.com

Sau parsing:
[
  {name: "John", age: 30, email: "john@example.com"},
  {name: "Jane", age: 25, email: "jane@example.com"}
]
```

### **Tại Sao Cần Parsing?**

```
✅ Lý Do:
   • File có format khác nhau (CSV, PDF, JSON, ...)
   • AI Agent cần dữ liệu có cấu trúc
   • Dữ liệu thô không thể dùng trực tiếp
   • Cần xác định ranh giới giữa các phần
   • Chuẩn bị để embedding & indexing
```

### **Các Format File Thường Gặp**

#### **1️⃣ CSV (Comma-Separated Values)**

#### **2️⃣ JSON (JavaScript Object Notation)**

#### **3️⃣ PDF**

#### **4️⃣ HTML/Markdown**

### **Parsing Methods trong AWS Bedrock**

Bedrock cung cấp các cách parse:

```
1️⃣ Automatic Parsing
   • Bedrock tự detect format
   • Tự chọn parser thích hợp
   • Quicker setup

2️⃣ Manual Selection
   • Chọn format explicitly
   • Cấu hình chi tiết
   • Kiểm soát tốt hơn

3️⃣ Custom Parsing
   • Lambda functions
   • Custom logic
   • Advanced cases
```

---

## Phần 2: Chunking

### **Chunking Là Gì?**

**Định nghĩa:**
```
Chunking = Quá trình chia file/text thành chunks nhỏ
• Chia dữ liệu lớn thành phần nhỏ
• Mỗi chunk ~ 500-2000 tokens
• Để embedding và indexing
• Kích thước hợp lý = tốc độ + chất lượng
```

**Ví Dụ:**
```
File gốc (5000 tokens):
"Long document with lots of content..."

Sau chunking (4 chunks):
Chunk 1 (1000 tokens): "Introduction and..."
Chunk 2 (1200 tokens): "Main content part 1..."
Chunk 3 (1300 tokens): "Main content part 2..."
Chunk 4 (1500 tokens): "Conclusion and..."
```

### **Tại Sao Cần Chunking?**

```
✅ Lý Do:
   • Embedding models có token limit
   • Chunks nhỏ → embedding nhanh hơn
   • Tăng tính liên quan (relevance)
   • Dễ retrieve chính xác
   • Tiết kiệm cost (ít tokens)
   • Cải thiện search quality
```

**So Sánh: Không Chunk vs Chunk**

```
❌ Không Chunk:
   • File 10,000 tokens → 1 embedding
   • Embedding rất generic
   • Hard to find specific info
   • Chậm, tốn nhiều tokens
   • Chi phí cao

✅ Có Chunk:
   • File 10,000 tokens → 5 chunks (2000 tokens mỗi)
   • Mỗi embedding specific
   • Dễ tìm exact info
   • Nhanh, ít tokens
   • Chi phí thấp
   • Chất lượng tốt hơn
```

### **Chunk Size - Cân Bằng Quan Trọng**

#### **Quá Nhỏ (< 500 tokens)**

```
Ưu điểm:
✅ Embedding cực kỳ specific
✅ Tìm kiếm chính xác
✅ Ít tokens

Nhược điểm:
❌ Quá nhiều chunks
❌ Context bị cắt (mất semantic)
❌ Tìm kiếm có thể miss
❌ Indexing lâu
❌ Chi phí tổng cao hơn
```

**Ví Dụ:**
```
Text: "John is a senior engineer. He has 10 years of experience."

Quá nhỏ (50 tokens/chunk):
Chunk 1: "John is a senior engineer."
Chunk 2: "He has 10 years of experience."

❌ Vấn đề:
   • "He" ở chunk 2 mà "John" ở chunk 1
   • Mất context
```

#### **Phù Hợp (1000-2000 tokens)**

```
Ưu điểm:
✅ Balance: specificity vs context
✅ Đủ context để hiểu
✅ Tìm kiếm tốt
✅ Embedding chất lượng
✅ Chi phí hợp lý

Nhược điểm:
❌ Medium specificity
```

**Ví Dụ:**
```
Text: "John is a senior engineer. He has 10 years of experience. 
His expertise includes cloud architecture and DevOps."

Phù hợp (200 tokens/chunk):
Chunk 1: "John is a senior engineer. He has 10 years of experience. 
His expertise includes cloud architecture and DevOps."

✅ Tốt:
   • Context đầy đủ
   • Semantic preserve
   • Tìm kiếm tốt
```

#### **Quá Lớn (> 3000 tokens)**

```
Ưu điểm:
✅ Ít chunks
✅ Context đầy đủ
✅ Embedding speed nhanh

Nhược điểm:
❌ Embedding quá generic
❌ Tìm kiếm không chính xác
❌ Tốn nhiều tokens
❌ Chi phí cao
❌ Chất lượng kém
```

**Ví Dụ:**
```
Text: "Long document 5000 tokens"

Quá lớn (1 chunk toàn bộ):
Chunk 1: "Long document 5000 tokens"

❌ Vấn đề:
   • Embedding represent toàn bộ
   • Mất chi tiết
   • Query không match chính xác
```


### **Overlapping trong Chunking**

**Overlap Là Gì?**

```
Overlap = Phần text trùng giữa các chunks liên tiếp
Mục đích: Giữ context liên tục
```

**Ví Dụ:**

```
Text gốc:
"The company was founded in 2020. It focuses on AI technology. 
The team has 50 engineers. They work on machine learning projects. 
Recently they launched a new product."

Chunk size: 50 tokens, No overlap:
Chunk 1: "The company was founded in 2020. It focuses on AI"
Chunk 2: "technology. The team has 50 engineers. They work on"
Chunk 3: "machine learning projects. Recently they launched a"
Chunk 4: "new product."

❌ Vấn đề:
   • "technology" bị cắt
   • Mất semantic

Chunk size: 50 tokens, 20% overlap (10 tokens):
Chunk 1: "The company was founded in 2020. It focuses on AI"
Chunk 2: "focuses on AI technology. The team has 50 engineers. They"
Chunk 3: "They work on machine learning projects. Recently they"
Chunk 4: "they launched a new product."

✅ Tốt:
   • Context liên tục
   • Semantic preserve
   • Tìm kiếm tốt hơn
```


### **Chunking Strategies**

#### **1️⃣ Fixed-Size Chunking**

```
Cách:
• Chia thành chunks kích thước cố định
• Ví dụ: 1000 tokens/chunk
• Dùng overlap

Code giả:
chunks = []
for i in range(0, text.length, chunk_size - overlap):
    chunk = text[i : i + chunk_size]
    chunks.append(chunk)

Ưu điểm:
✅ Đơn giản, nhanh
✅ Dễ implement

Nhược điểm:
❌ Có thể cắt giữa câu
❌ Mất semantic
```

#### **2️⃣ Sentence-Based Chunking**

```
Cách:
• Chia theo câu (sentences)
• Mỗi chunk = 5-10 sentences
• Preserve sentence boundaries

Code giả:
sentences = split_by_sentence(text)
chunks = []
i = 0
while i < len(sentences):
    chunk = " ".join(sentences[i:i+5])
    chunks.append(chunk)
    i += 5

Ưu điểm:
✅ Preserve semantic
✅ Natural boundaries

Nhược điểm:
❌ Chunk size không fixed
❌ Phức tạp hơn
```

#### **3️⃣ Semantic Chunking (Advanced)**

```
Cách:
• Dùng AI để hiểu semantic
• Chia tại "natural breaks"
• Preserve meaning

Quá trình:
1. Compute embeddings của sentences
2. Tìm similarity giữa sentences
3. Chia tại low-similarity points

Ưu điểm:
✅ Best quality
✅ Semantic aware

Nhược điểm:
❌ Complex, expensive
❌ Slow
```

#### **4️⃣ Hierarchical Chunking**

```
Cách:
• Tính đến document structure
• Sections, subsections, ...
• Multi-level chunks

Ví dụ:
Document:
  Section 1
    Subsection 1.1
    Subsection 1.2
  Section 2
    Subsection 2.1

Chunks:
1. Section 1 content
2. Section 1.1 content
3. Section 1.2 content
4. ...

Ưu điểm:
✅ Respect structure
✅ Better organization

Nhược điểm:
❌ Cần detect structure
```

