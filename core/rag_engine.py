import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class InMemoryRAGEngine:
    """Lightweight in-memory vector indexing and semantic retrieval engine."""
    def __init__(self):
        self.documents = []
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.doc_vectors = None
        self.is_indexed = False

    def index_documents(self, documents: list[dict]):
        """Indexes a list of EvidenceDocument dictionaries."""
        self.documents = documents
        if not documents:
            self.is_indexed = False
            return
            
        corpus = [f"{doc.get('title', '')} {doc.get('content', '')} {doc.get('doc_type', '')}" for doc in documents]
        self.doc_vectors = self.vectorizer.fit_transform(corpus)
        self.is_indexed = True

    def search(self, query: str, customer_id: str = None, top_k: int = 3) -> list[dict]:
        """Searches documents matching the query, optionally filtering by customer_id."""
        if not self.is_indexed or not self.documents:
            return []
            
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.doc_vectors).flatten()
        
        ranked_indices = similarities.argsort()[::-1]
        results = []
        
        for idx in ranked_indices:
            doc = self.documents[idx]
            score = float(similarities[idx])
            
            # Optional customer filtering
            if customer_id and doc.get("customer_id") != customer_id:
                continue
                
            results.append({
                **doc,
                "similarity_score": round(max(0.05, score), 3)
            })
            
            if len(results) >= top_k:
                break
                
        return results

    def format_evidence_for_prompt(self, evidence_docs: list[dict]) -> str:
        """Formats retrieved documents into a clean context block for LLM system prompts."""
        if not evidence_docs:
            return "No specific interaction history retrieved."
            
        formatted_blocks = []
        for i, doc in enumerate(evidence_docs, 1):
            formatted_blocks.append(
                f"[Evidence #{i} | {doc.get('doc_type', 'Record')} | Date: {doc.get('date', 'N/A')} | Relevance: {doc.get('similarity_score', 0.0)*100:.0f}%]\n"
                f"Title: {doc.get('title')}\n"
                f"Excerpt: {doc.get('content')}"
            )
        return "\n\n".join(formatted_blocks)
