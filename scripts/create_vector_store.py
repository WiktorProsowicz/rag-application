"""Utility script to build a local vector store from documents."""

from __future__ import annotations

import argparse
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


def load_documents(path: Path):
    loader = DirectoryLoader(
        str(path),
        glob="**/*",
        loader_cls=lambda p: PyPDFLoader(p) if Path(p).suffix.lower() == ".pdf" else TextLoader(p, encoding="utf-8"),
    )
    return loader.load()


def create_vector_store(doc_path: Path, persist_dir: Path) -> None:
    docs = load_documents(doc_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Chroma.from_documents(chunks, embedder, persist_directory=str(persist_dir)).persist()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a local Chroma vector store")
    parser.add_argument("--data", type=Path, default=Path("documents"), help="Folder with source documents")
    parser.add_argument("--out", type=Path, default=Path("vector_store"), help="Output directory for the vector store")
    args = parser.parse_args()

    persist = args.out
    persist.mkdir(parents=True, exist_ok=True)
    create_vector_store(args.data, persist)
    print(f"Vector store created in {persist}")
