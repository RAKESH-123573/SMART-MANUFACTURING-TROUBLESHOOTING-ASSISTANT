import os
from typing import List
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

CHROMA_DIR = os.path.join(os.path.dirname(__file__), '..', '.chroma_db')


def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    texts = []
    for p in reader.pages:
        try:
            texts.append(p.extract_text() or "")
        except Exception:
            continue
    return "\n".join(texts)


def ingest_pdf(path: str):
    """Load PDF, split, embed and persist to Chroma vectorstore."""
    text = extract_text_from_pdf(path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_text(text)
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_texts(docs, embeddings, persist_directory=CHROMA_DIR)
    vectordb.persist()


def retrieve(query: str, k: int = 4) -> List[dict]:
    """Return top-k documents with simple metadata."""
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    results = vectordb.similarity_search_with_score(query, k=k)
    out = []
    for doc, score in results:
        out.append({"page_content": doc.page_content, "score": float(score)})
    return out
