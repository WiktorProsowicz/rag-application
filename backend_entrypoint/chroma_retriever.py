"""LangChain-based retriever using a persisted Chroma vector store."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


@dataclass
class ChromaRetriever:
    db: Chroma

    @classmethod
    def from_persisted(
        cls, path: str, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ) -> "ChromaRetriever":
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        db = Chroma(persist_directory=path, embedding_function=embeddings)
        return cls(db)

    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, object]]:
        """Return the top *k* matching documents."""
        results = self.db.similarity_search_with_score(query, k=k)
        return [
            {"text": doc.page_content, "score": score, "metadata": doc.metadata}
            for doc, score in results
        ]
