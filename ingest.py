"""Ingest notes, PDFs, and URLs into the knowledge base."""
import argparse, glob, os
from pathlib import Path
from src.kb import KnowledgeBase

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", nargs="+", required=True, help="Files, directories, or URLs to ingest")
    parser.add_argument("--model", default="nomic-embed-text", help="Ollama embedding model")
    args = parser.parse_args()

    kb = KnowledgeBase(embedding_model=args.model)
    total = 0
    for source in args.source:
        if source.startswith("http"):
            n = kb.ingest_url(source)
        elif os.path.isdir(source):
            for f in Path(source).rglob("*"):
                if f.suffix in (".md", ".txt", ".pdf"):
                    n = kb.ingest_file(str(f))
                    total += n
        else:
            for f in glob.glob(source):
                n = kb.ingest_file(f)
                total += n
    print(f"Ingested {total} chunks into knowledge base")

if __name__ == "__main__":
    main()
