from typing import Dict

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import JsonOutputParser

from rag.schemas import Module
from rag.types import MODE_MAPPING, ModeType
from rag.utils import get_vectorstore, load_config, load_prompt


def get_rag_response(topic: str, mode: ModeType) -> Dict:
    """
    Gets the response from the Retrieval Augmented Generation (RAG) pipeline.

    Parameters:
    -----------
    topic: str
        The topic for which the response is generated.
    mode: str
        The mode to be used for the pipeline (e.g., 'chapter', 'section').

    Returns:
    --------
    answer: Dict
        Dictionary containing the generated response and source documents.
    """
    config = load_config("configs/config.yaml")

    parser = JsonOutputParser(pydantic_object=Module)
    prompt = PromptTemplate.from_template(load_prompt()).partial(
        mode=MODE_MAPPING[mode],
        format_instructions=parser.get_format_instructions(),
        format_keys=str(list(Module.__fields__.keys())),
        format_count=str(len(Module.__fields__.keys())),
    )
    model = Ollama(
        model=config.LLM_NAME,
        format="json",
        temperature=config.LLM_TEMPERATURE,
        top_p=config.LLM_TOP_P,
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=model,
        retriever=get_vectorstore(as_retriever=True),
        chain_type_kwargs={"prompt": prompt},
        chain_type="stuff",
        return_source_documents=True,
    )

    qa_chain_result = qa_chain.invoke(topic)
    # TODO: incorporate parser into the chain itself
    # force parsing to JSON (for now...)
    qa_chain_result["result"] = parser.parse(qa_chain_result["result"])

    return qa_chain_result
