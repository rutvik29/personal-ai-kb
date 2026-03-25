"""Local knowledge base with Ollama + ChromaDB."""
import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from typing import List
import requests


RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant answering questions from the user's personal knowledge base. Use only the provided context. If the answer is not in the context, say so."),
    ("human", "Context from knowledge base:\n{context}\n\nQuestion: {question}")
])


class KnowledgeBase:
    def __init__(self, collection_name: str = "personal_kb", embedding_model: str = "nomic-embed-text", llm_model: str = "llama3.2", persist_dir: str = "./kb_data"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        ef = OllamaEmbeddingFunction(url="http://localhost:11434/api/embeddings", model_name=embedding_model)
        self.collection = self.client.get_or_create_collection(collection_name, embedding_function=ef)
        self.llm = OllamaLLM(model=llm_model)
        self.chain = RAG_PROMPT | self.llm

    def ingest_file(self, file_path: str) -> int:
        import hashlib
        from pathlib import Path
        p = Path(file_path)
        if p.suffix == ".pdf":
            try:
                import pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            except Exception:
                return 0
        else:
            text = p.read_text(encoding="utf-8", errors="ignore")
        chunks = [text[i:i+1000] for i in range(0, len(text), 800)]
        ids = [hashlib.md5(f"{file_path}_{i}".encode()).hexdigest() for i in range(len(chunks))]
        if chunks:
            self.collection.add(documents=chunks, ids=ids, metadatas=[{"source": str(file_path), "chunk": i} for i in range(len(chunks))])
        return len(chunks)

    def ingest_url(self, url: str) -> int:
        import hashlib
        try:
            resp = requests.get(url, timeout=10)
            text = resp.text[:10000]
            chunks = [text[i:i+1000] for i in range(0, len(text), 800)]
            ids = [hashlib.md5(f"{url}_{i}".encode()).hexdigest() for i in range(len(chunks))]
            self.collection.add(documents=chunks, ids=ids, metadatas=[{"source": url, "chunk": i} for i in range(len(chunks))])
            return len(chunks)
        except Exception:
            return 0

    def search(self, query: str, k: int = 5) -> List[dict]:
        results = self.collection.query(query_texts=[query], n_results=k)
        return [{"content": doc, "source": meta.get("source",""), "score": 1 - dist}
                for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0])]

    def chat(self, question: str) -> str:
        results = self.search(question)
        context = "\n\n".join(f"[{r['source']}]\n{r['content']}" for r in results)
        return self.chain.invoke({"context": context, "question": question})
