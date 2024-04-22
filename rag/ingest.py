from typing import List

from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.utils import calculate_chunk_ids, get_vectorstore


def load_documents(data_path: str) -> List[Document]:
    """
    Loads documents (PDF files) from the specified directory.

    Parameters:
    -----------
    data_path: str
        Path to the directory containing PDF files.

    Returns:
    --------
    documents: List[Document]
        List of loaded documents.
    """
    loader = PyPDFDirectoryLoader(data_path)
    return loader.load()


def split_documents(
    documents: List[Document], chunk_size: int, chunk_overlap: int
) -> List[Document]:
    """
    Splits the documents into smaller chunks.

    Parameters:
    -----------
    documents: List[Document]
        List of documents to be split.
    chunk_size: int
        Maximum length of each chunk.
    chunk_overlap: int
        Number of overlapping characters between chunks.

    Returns:
    --------
    chunks: List[Document]
        List of document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return text_splitter.split_documents(documents)


def ingest_documents(documents: List[Document]):
    """
    Ingests the documents into the Chroma vector store.

    Parameters:
    -----------
    documents: List[Document]
        List of documents to be ingested.
    """
    vectorstore = get_vectorstore()

    chunks_with_ids = calculate_chunk_ids(documents)
    existing_ids = set(vectorstore.get(include=[])["ids"])
    new_chunks = [
        chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids
    ]

    if new_chunks:
        print(f"   👉 Adicionando {len(new_chunks)} novos documentos")
        vectorstore.add_documents(
            new_chunks, ids=[chunk.metadata["id"] for chunk in new_chunks]
        )
        vectorstore.persist()
    else:
        print("   ✅ Nenhum novo documento para adicionar")
