import os
import gc
import tempfile
import uuid
import pandas as pd

from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.core import PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.readers.docling import DoclingReader
from llama_index.core.node_parser import MarkdownNodeParser

import streamlit as st

# ---- Session state setup ----
if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}

session_id = st.session_state.id
client = None

# ---- Excel file path ----
EXCEL_PATH = r"C:\Users\Aditi Desai\OneDrive\Desktop\SIH_project\data\CentralReport1757836845759.xlsx"

@st.cache_resource
def load_llm():
    llm = Gemini(model="models/gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
    return llm

def reset_chat():
    st.session_state.messages = []
    st.session_state.context = None
    gc.collect()

def display_excel(file_path):
    st.markdown("### Excel Preview")
    df = pd.read_excel(file_path)
    st.dataframe(df)

# ---- Load and index Excel directly ----
if os.path.exists(EXCEL_PATH):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, os.path.basename(EXCEL_PATH))
            with open(EXCEL_PATH, "rb") as src, open(file_path, "wb") as dst:
                dst.write(src.read())

            file_key = f"{session_id}-{os.path.basename(EXCEL_PATH)}"
            st.write("Indexing your document...")

            if file_key not in st.session_state.get("file_cache", {}):
                reader = DoclingReader()
                loader = SimpleDirectoryReader(
                    input_dir=temp_dir,
                    file_extractor={".xlsx": reader},
                )
                docs = loader.load_data()

                llm = load_llm()
                embed_model = HuggingFaceEmbedding(
                    model_name="BAAI/bge-large-en-v1.5", trust_remote_code=True
                )
                Settings.embed_model = embed_model
                node_parser = MarkdownNodeParser()
                index = VectorStoreIndex.from_documents(
                    documents=docs, transformations=[node_parser], show_progress=True
                )

                Settings.llm = llm
                query_engine = index.as_query_engine(streaming=True)

                qa_prompt_tmpl_str = (
                    "Context information is below.\n"
                    "---------------------\n"
                    "{context_str}\n"
                    "---------------------\n"
                    "Given the context information above I want you to think step by step to answer the query "
                    "in a highly precise and crisp manner focused on the final answer, "
                    "incase case you don't know the answer say 'I don't know!'.\n"
                    "Query: {query_str}\n"
                    "Answer: "
                )
                qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)

                query_engine.update_prompts(
                    {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
                )

                st.session_state.file_cache[file_key] = query_engine
            else:
                query_engine = st.session_state.file_cache[file_key]

            st.success("Ready to Chat!")
            display_excel(EXCEL_PATH)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()
else:
    st.error(f"Excel file not found at: {EXCEL_PATH}")
    st.stop()

# ---- UI Layout ----
col1, col2 = st.columns([6, 1])

with col1:
    st.header("Chat with Excel using Docling 🐥 & Gemini-1.5")

with col2:
    st.button("Clear ↺", on_click=reset_chat)

if "messages" not in st.session_state:
    reset_chat()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask something about the Excel file..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        streaming_response = query_engine.query(prompt)

        for chunk in streaming_response.response_gen:
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
