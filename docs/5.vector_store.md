## Tổng quan tài liệu

Tài liệu này giải thích khái niệm **Vector Store** - thành phần quan trọng trong Knowledge Base của AI Agent. Hiểu Vector Store giúp bạn xây dựng Knowledge Base hiệu quả hơn.

---

## Phần 1: Khái Niệm Cơ Bản

### **Vector Store Là Gì?**

**Định nghĩa:**
```
Vector Store = Database đặc biệt lưu trữ & tìm kiếm vectors
• Lưu embeddings (vector representations) của dữ liệu
• Hỗ trợ tìm kiếm tương tự (similarity search)
• Tối ưu cho high-dimensional data
• Cho phép truy vấn nhanh
```

**Ví Dụ Đơn Giản:**
```
Database Thường:
┌─────┬──────────┬──────────┐
│ ID  │ Name     │ Price    │
├─────┼──────────┼──────────┤
│ 1   │ Product1 │ $100     │
│ 2   │ Product2 │ $200     │
└─────┴──────────┴──────────┘

Vector Store:
┌─────┬────────────────────────────┐
│ ID  │ Vector (Embedding)         │
├─────┼────────────────────────────┤
│ 1   │ [0.25, 0.87, 0.43, ...]   │
│ 2   │ [0.28, 0.91, 0.41, ...]   │
└─────┴────────────────────────────┘

Khác nhau:
• Thường: Lưu text, numbers, dates
• Vector: Lưu meaning (semantic) của text
```

### **Tại Sao Cần Vector Store?**

```
✅ Lý Do Quan Trọng:

1. Semantic Search
   └─ Tìm kiếm theo ý nghĩa, không chỉ keyword
   └─ "recommend product" ~ "suggest items"

2. Similarity Search
   └─ Tìm items tương tự
   └─ Query vector gần vector nào

3. Fast Retrieval
   └─ Dùng indexing & hashing
   └─ O(log n) instead of O(n)

4. Dimensionality Reduction
   └─ Lưu essence của text trong vectors
   └─ Giảm dung lượng

5. Multi-Modal Support
   └─ Có thể lưu embeddings từ text, image, audio

6. AI-Ready
   └─ LLMs sử dụng embeddings natively
   └─ Tích hợp tốt với AI models
```

---

## Phần 2: Embeddings & Vectors

### **Embedding Là Gì?**

**Định nghĩa:**
```
Embedding = Biểu diễn số (vector) của text/data
• Chuyển text thành vector số
• Preserve semantic meaning
• Có thể tính similarity
```

**Quá Trình:**
```
Text: "I like machine learning"
       ↓
   Embedding Model
   (e.g., Titan, OpenAI, Cohere)
       ↓
Vector: [0.1, 0.8, 0.3, 0.2, ..., 0.5]
        (1536 dimensions cho một số model)
```

### **Vector Representation**

**1️⃣ Vector Dimensions**

```
Vector có bao nhiêu dimensions?

Thường: 300-1536 dimensions

Ví dụ:
• 300 dimensions: Nhỏ, nhanh, rẻ
  └─ Phù hợp: Simple tasks
  
• 768 dimensions: Medium, balanced
  └─ Phù hợp: Tổng quát (recommend)
  
• 1536 dimensions: Lớn, expensive
  └─ Phù hợp: Complex tasks, high accuracy

Cho lab: 1024 dimensions (Titan Embeddings V2)
```

**2️⃣ Vector Values**

```
Mỗi dimension = 1 số (float)

Ví dụ vector 5 dimensions:
[0.23, -0.81, 0.15, 0.92, -0.31]

Ý nghĩa:
• Mỗi số = feature của text
• Combine tất cả = semantic meaning
• Không human-readable, nhưng machine-readable
```

**3️⃣ Vector Distance (Similarity)**

```
Hai text gần nhau → vectors gần nhau

Ví dụ:
Text 1: "I like machine learning"
Vector 1: [0.1, 0.8, 0.3, ...]

Text 2: "I enjoy AI and ML"
Vector 2: [0.12, 0.82, 0.28, ...]

Distance: 0.05 (rất gần)

Text 3: "What is cooking?"
Vector 3: [0.5, 0.2, 0.9, ...]

Distance: 1.2 (khác xa)

→ Similarity = 1 / (1 + distance)
```

### **Embedding Models**

**Thường Dùng:**

| Model | Provider | Dimensions | Speed | Cost | Best For |
|-------|----------|-----------|-------|------|----------|
| **Titan V2** | AWS | 1024 | Fast | $ | Balanced |
| **OpenAI** | OpenAI | 1536 | Medium | $$ | General |
| **Cohere** | Cohere | 768-1024 | Fast | $ | Specific |
| **BGE** | BAAI | 768 | Very Fast | Free | Production |
| **MiniLM** | Microsoft | 384 | Super Fast | Free | Lightweight |

**Cho Lab (Recommend):**
```
AWS Titan Embeddings V2
• Dimensions: 1024
• Speed: Fast
• Cost: Reasonable
• Vietnamese support: Yes
• Multi-language: Yes
```

---

## Phần 3: Vector Store Architecture

### **Thành Phần Chính**

```
Vector Store Components:

1. Embedding Layer
   └─ Convert text → vectors
   
2. Index/Storage Layer
   └─ Lưu vectors efficiently
   
3. Search Layer
   └─ Find similar vectors quickly
   
4. Metadata Storage
   └─ Lưu source info, timestamps, etc
```

### **Architecture Diagram**

```
┌─────────────────────────────────────────────────────┐
│                   Vector Store                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Input: Text/Data                                  │
│    ↓                                               │
│  ┌─────────────────────────────────┐               │
│  │ 1. Embedding Layer              │               │
│  │ (Text → Vector)                 │               │
│  │ Model: Titan, OpenAI, etc       │               │
│  └────────────┬────────────────────┘               │
│               │                                     │
│               ↓                                     │
│  ┌─────────────────────────────────┐               │
│  │ 2. Normalization                │               │
│  │ (Scale vectors to unit length)  │               │
│  └────────────┬────────────────────┘               │
│               │                                     │
│               ↓                                     │
│  ┌─────────────────────────────────┐               │
│  │ 3. Indexing                     │               │
│  │ (Organize vectors for search)   │               │
│  │ Methods: HNSW, IVF, LSH, ...   │               │
│  └────────────┬────────────────────┘               │
│               │                                     │
│               ↓                                     │
│  ┌─────────────────────────────────┐               │
│  │ 4. Storage                      │               │
│  │ Vector DB: Pinecone, Milvus,   │               │
│  │            Weaviate, Chroma     │               │
│  └────────────┬────────────────────┘               │
│               │                                     │
│  ─────────────┴─────────────────                   │
│  │ Vectors  │ Metadata │ Index │                  │
│  └──────────┴──────────┴───────┘                  │
│                                                     │
│  Query: Text                                       │
│    ↓                                               │
│  Embedding: vector_query                           │
│    ↓                                               │
│  Search: Find Top-K Similar                        │
│    ↓                                               │
│  Return: [Result1, Result2, ...]                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Phần 4: Vector Search Process

### **Similarity Search Là Gì?**

**Quá Trình:**
```
1. User Query
   "Recommend products for loyal customers"
   
2. Embed Query
   query_vector = embedding_model(query)
   query_vector = [0.2, 0.9, 0.1, ..., 0.7]
   
3. Search Vector Store
   Find vectors closest to query_vector
   
4. Calculate Distance
   distance = ||query_vector - stored_vector||
   
5. Sort by Distance
   Top-K results (K=3, 5, 10, ...)
   
6. Return Results
   [
     {text: "Product A", score: 0.95},
     {text: "Product B", score: 0.87},
     {text: "Product C", score: 0.82}
   ]
```

### **Distance Metrics**

**1️⃣ Euclidean Distance (L2)**

```
Công thức:
d = √[(x1-y1)² + (x2-y2)² + ... + (xn-yn)²]

Ví dụ:
vector1 = [0.1, 0.8]
vector2 = [0.2, 0.7]

d = √[(0.1-0.2)² + (0.8-0.7)²]
  = √[0.01 + 0.01]
  = √0.02
  = 0.141

Đặc điểm:
✅ Intuitive, easy to understand
✅ Precise measurements
❌ Slow for high dimensions
```

**2️⃣ Cosine Similarity (Thường Dùng)**

```
Công thức:
similarity = (A · B) / (||A|| × ||B||)

Ý nghĩa:
• Angle giữa 2 vectors
• Range: -1 (opposite) to 1 (identical)
• Thường dùng: 0 to 1 (normalized)

Ví dụ:
vector1 = [0.1, 0.8]
vector2 = [0.2, 0.7]

similarity ≈ 0.998 (rất tương tự)

Đặc điểm:
✅ Fast, even for high dimensions
✅ Normalize cho magnitude
✅ Industry standard
❌ Angle-based, not distance-based
```

**3️⃣ Dot Product**

```
Công thức:
dot = A · B = a1×b1 + a2×b2 + ... + an×bn

Ví dụ:
vector1 = [0.1, 0.8]
vector2 = [0.2, 0.7]

dot = 0.1×0.2 + 0.8×0.7 = 0.58

Đặc điểm:
✅ Fastest
✅ Good for normalized vectors
❌ Depends on magnitude
```

**Recommend cho Lab:**
```
Dùng: Cosine Similarity
Lý do:
✅ Fast
✅ Thích hợp embeddings
✅ AWS Bedrock default
✅ Insensitive to magnitude
```

### **Top-K Retrieval**

```
Ý nghĩa:
Lấy K vectors gần nhất (most similar)

Thường dùng K:
• K=1: Tìm exact match
• K=3-5: Balanced (recommend)
• K=10: Broad retrieval
• K=50: Very broad

Cách chọn K:
• Context window nhỏ → K nhỏ (3-5)
• Context window lớn → K lớn (10-20)
• Cho lab: K=3-5 tối ưu
```
