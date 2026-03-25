"""CLI chat with your knowledge base."""
import sys
from src.kb import KnowledgeBase

if __name__ == "__main__":
    kb = KnowledgeBase()
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Ask your knowledge base: ")
    answer = kb.chat(q)
    print(f"\n{answer}")
