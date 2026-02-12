from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Tuple
import logging

logger = logging.getLogger("remo_ai")

def vector_only_search(db: Session, query_embedding: list, limit: int) -> List[Tuple[str, float]]:
    """Pure vector similarity search"""
    sql = text("""
        SELECT content, 1 - (embedding <=> CAST(:embedding AS vector)) as score
        FROM documents
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
    """)
    results = db.execute(sql, {"embedding": str(query_embedding), "limit": limit}).fetchall()
    return [(row[0], row[1]) for row in results]

def fulltext_only_search(db: Session, query: str, limit: int) -> List[Tuple[str, float]]:
    """Pure BM25 full-text search"""
    sql = text("""
        SELECT content, ts_rank(content_tsv, websearch_to_tsquery('english', :query)) as score
        FROM documents
        WHERE content_tsv @@ websearch_to_tsquery('english', :query)
        ORDER BY score DESC
        LIMIT :limit
    """)
    results = db.execute(sql, {"query": query, "limit": limit}).fetchall()
    return [(row[0], row[1]) for row in results]

def hybrid_rrf_search(db: Session, query_embedding: list, query: str, limit: int, k: int = 60) -> List[Tuple[str, float]]:
    """Hybrid search with Reciprocal Rank Fusion (RRF)"""
    sql = text("""
        WITH vector_search AS (
            SELECT id, content,
                ROW_NUMBER() OVER (ORDER BY embedding <=> CAST(:embedding AS vector)) AS rank
            FROM documents
        ),
        text_search AS (
            SELECT id, content,
                ROW_NUMBER() OVER (ORDER BY ts_rank(content_tsv, websearch_to_tsquery('english', :query)) DESC) AS rank
            FROM documents
            WHERE content_tsv @@ websearch_to_tsquery('english', :query)
        )
        SELECT 
            COALESCE(v.content, t.content) AS content,
            COALESCE(1.0 / (:k + v.rank), 0.0) + COALESCE(1.0 / (:k + t.rank), 0.0) AS score
        FROM vector_search v
        FULL OUTER JOIN text_search t ON v.id = t.id
        ORDER BY score DESC
        LIMIT :limit
    """)
    results = db.execute(sql, {
        "embedding": str(query_embedding),
        "query": query,
        "k": k,
        "limit": limit
    }).fetchall()
    return [(row[0], row[1]) for row in results]
