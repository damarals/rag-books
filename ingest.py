from rag.ingest import ingest_documents, load_documents, split_documents
from rag.utils import load_config

if __name__ == "__main__":
    config = load_config("configs/config.yaml")

    print("📚 Carregando documentos...")
    documents = load_documents(config.DATA_PATH)

    print("🔍 Dividindo documentos...")
    chunks = split_documents(documents, config.CHUNK_SIZE, config.CHUNK_OVERLAP)

    print("🚀 Adicionando ao vector store")
    ingest_documents(chunks)
