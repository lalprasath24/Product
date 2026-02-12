# Hybrid Search Implementation Guide

## What Was Implemented

### 1. Database Schema Updates
- Added `content_tsv` column (TSVECTOR) for full-text search
- Created GIN index on `content_tsv` for fast BM25 keyword search
- Created HNSW index on `embedding` for fast vector similarity search

### 2. Automatic Full-Text Indexing
- PostgreSQL trigger automatically updates `content_tsv` when documents are inserted/updated
- Uses English language stemming and stop words

### 3. Hybrid Search Strategy
**Reciprocal Rank Fusion (RRF)** - Industry standard for combining rankings:
- Formula: `score = 1/(k + rank_vector) + 1/(k + rank_fulltext)`
- k=60 is the standard constant (balances contribution of both methods)
- Combines results from both search methods fairly

## Why This Approach?

### Pure Vector Search (Old)
❌ Expensive for large datasets
❌ Misses exact keyword matches
❌ Struggles with rare terms

### Pure Keyword Search (BM25)
❌ Misses semantic meaning
❌ No understanding of synonyms
❌ Poor for conceptual queries

### Hybrid Search (New) ✅
✅ Best of both worlds
✅ Handles exact matches AND semantic similarity
✅ Production-ready for large datasets
✅ Used by major search engines

## Search Modes Available

### 1. Hybrid Search (Default - Recommended)
```python
from app.services.database import search_documents
results = await search_documents("your query", limit=5)
```

### 2. Vector-Only Search
```python
from app.services.search_utils import vector_only_search
results = vector_only_search(db, query_embedding, limit=5)
```

### 3. Full-Text Only Search
```python
from app.services.search_utils import fulltext_only_search
results = fulltext_only_search(db, "your query", limit=5)
```

## Performance Optimizations

1. **HNSW Index** - O(log n) vector search instead of O(n)
2. **GIN Index** - Fast full-text search with inverted index
3. **Trigger-based indexing** - No manual updates needed
4. **Efficient RRF** - Single query combines both methods

## Query Examples

### Good for Vector Search
- "How do I improve performance?" (semantic)
- "What are the benefits?" (conceptual)

### Good for Keyword Search
- "API endpoint /users" (exact terms)
- "error code 500" (specific identifiers)

### Best with Hybrid
- "database connection issues" (both semantic + keywords)
- "authentication best practices" (concepts + terms)

## Migration Steps

If you have existing data:
1. Restart your application (trigger will be created)
2. Update existing documents to populate `content_tsv`:
```sql
UPDATE documents SET content = content;
```

## Monitoring

Check if indexes are being used:
```sql
EXPLAIN ANALYZE
SELECT * FROM documents 
WHERE content_tsv @@ websearch_to_tsquery('english', 'your query');
```

Should show "Bitmap Index Scan on documents_content_tsv_idx"
