import os
import box
import yaml
import contextlib
from typing import Dict, List

from langchain_community.embeddings.huggingface import HuggingFaceInstructEmbeddings
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever

from rag.prompts import PROMPT_MODULE


def suppress_stdout(func):
    """
    Suppresses the standard output of the decorated function.

    Parameters:
    -----------
    func: Callable
        Function to be decorated.

    Returns:
    --------
    wrapper: Callable
        Decorated function.
    """

    def wrapper(*args, **kwargs):
        with open(os.devnull, "w") as devnull:
            with contextlib.redirect_stdout(devnull):
                return func(*args, **kwargs)

    return wrapper


def load_config(config_path: str) -> Dict:
    """
    Loads the configuration from the specified YAML file.

    Parameters:
    -----------
    config_path: str
        Path to the YAML configuration file.

    Returns:
    --------
    config: Dict
        Dictionary containing the configuration settings.
    """
    with open(config_path, "r", encoding="utf8") as file:
        return box.Box(yaml.safe_load(file))


@suppress_stdout
def get_embedding_function() -> HuggingFaceInstructEmbeddings:
    """
    Gets the embedding function for the Chroma vector store.

    Returns:
    --------
    embedding_function: HuggingFaceInstructEmbeddings
        Embedding function to be used by the Chroma vector store.
    """
    config = load_config("configs/config.yaml")
    return HuggingFaceInstructEmbeddings(
        model_name=config.EMBEDDING_MODEL_NAME,
        model_kwargs={"device": config.EMBEDDING_DEVICE},
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vectorstore(as_retriever: bool = False) -> VectorStoreRetriever:
    """
    Gets the Chroma vector store instance.

    Parameters:
    -----------
    as_retriever: bool, optional
        Whether to return the vector store as a retriever. Default is False.

    Returns:
    --------
    vectorstore: VectorStore
        Chroma vector store instance.
    """
    config = load_config("configs/config.yaml")
    vectorstore = Chroma(
        persist_directory=config.CHROMA_PATH,
        embedding_function=get_embedding_function(),
    )

    if as_retriever:
        return vectorstore.as_retriever(search_kwargs={"k": config.RETRIEVER_TOP_K})
    return vectorstore


def load_prompt() -> str:
    """
    Loads the prompt template from the specified file.

    Returns:
    --------
    prompt: str
        Prompt template as a string.
    """
    return PROMPT_MODULE


def calculate_chunk_ids(chunks: List[Document]) -> List[Document]:
    """
    Calculates and assigns unique IDs to each document chunk.

    Parameters:
    -----------
    chunks: List[Document]
        List of document chunks.

    Returns:
    --------
    chunks_with_ids: List[Document]
        List of document chunks with assigned IDs.
    """
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        # Page Source : Page Number : Chunk Index
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks
