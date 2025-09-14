# Standard library
import os

# Third-party libraries
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.core.memory import ChatSummaryMemoryBuffer
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain_community.embeddings import HuggingFaceEmbeddings

# Local/project imports
import prompts


def load_chat_engine():
    # Step 1: Load env and set OpenAI key
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    # Step 2: Set embedding model (supports Traditional Chinese)
    embedding_model = LangchainEmbedding(
        HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
    )

    # Step 3: Set LLM (OpenAI GPT-4)
    llm = OpenAI(
        model="gpt-4",
        temperature=1.0,
        max_tokens=300,
        system_prompt=(prompts.SYSTEM_PROMPT_2)
    )

    # Step 4: Configure global Settings
    Settings.llm = llm
    Settings.embed_model = embedding_model
    Settings.node_parser = SentenceSplitter(chunk_size=200, chunk_overlap=20)

    # Step 5: Load documents
    documents = SimpleDirectoryReader("rag_input/mel/").load_data()

    # Step 6: Create index
    index = VectorStoreIndex.from_documents(documents)

    # Step 7: Create retriever
    retriever = index.as_retriever(similarity_top_k=5)

    # Step 8: Create conversation memory
    memory = ChatSummaryMemoryBuffer.from_defaults(token_limit=1500)

    # Step 9: Create chat engine
    chat_engine = ContextChatEngine.from_defaults(
        retriever=retriever,
        memory=memory,
        llm=llm,
        system_prompt=llm.system_prompt
    )

    return chat_engine
