import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
import os

# --- 1. Database Connection ---
def connect_database(db_file_path):
    """Establishes and returns a connection to the SQLite database."""
    try:
        if not os.path.exists(db_file_path):
            st.error(f"Error: Database file '{db_file_path}' not found. Please create it first.")
            return None
        
        sqlite_uri = f"sqlite:///{db_file_path}"
        db = SQLDatabase.from_uri(sqlite_uri)
        return db
    except Exception as e:
        st.error(f"Connection failed: {e}")
        return None

# --- 2. Database Operations ---
def run_query(query):
    """Runs a SQL query against the connected database."""
    if "db" in st.session_state and st.session_state.db:
        try:
            return st.session_state.db.run(query)
        except Exception as e:
            return f"Query failed: {e}. Please check the SQL syntax and table/column names."
    return "Error: Please connect to the database first."

def get_database_schema():
    """Fetches the schema of the connected database."""
    if "db" in st.session_state and st.session_state.db:
        return st.session_state.db.get_table_info(table_names=['central_report_full'])
    return "Error: Please connect to the database first."

# --- 3. LLM and Prompt Engineering ---
llm = ChatOllama(model="phi3:mini")

def get_query_from_llm(question):
    """Generates a SQL query from a user's question using an LLM."""
    
    # --- EDITED SECTION 1: This prompt is now much more specific and includes examples ---
    template = """
    You are a SQLite expert. Given a user's question, you must generate a syntactically correct SQLite query.
    Your response must be ONLY the SQL query. Do not include any other text, explanations, or markdown formatting.

    Use the following schema for the `central_report_full` table:
    {schema}

    **Examples:**

    - Question: How many states are in the report?
      SQL query: SELECT COUNT(DISTINCT STATE) FROM central_report_full;

    - Question: list the top 3 districts with the highest total rainfall
      SQL query: SELECT DISTRICT, Rainfall_mm_Total FROM central_report_full ORDER BY Rainfall_mm_Total DESC LIMIT 3;

    **Your Turn:**

    - Question: {question}
      SQL query:
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    response = chain.invoke({"question": question, "schema": get_database_schema()})
    return response.content.strip().replace("```sql", "").replace("```", "")

def get_response_for_query_result(question, query, result):
    """Generates a natural language response from the SQL query and its result."""

    # --- EDITED SECTION 2: This prompt has also been improved with examples ---
    template2 = """
    Given the user's question, the SQL query that was run, and the result of the query, write a conversational, natural language response.

    **Examples:**

    - Question: How many states are covered in the report?
      SQL query: SELECT COUNT(DISTINCT STATE) FROM central_report_full;
      Result: [(19,)]
      Response: The report includes data for 19 different states.

    - Question: What is the total groundwater extraction in the NICOBAR district?
      SQL query: SELECT Total_Current_GW_Extraction_ham FROM central_report_full WHERE DISTRICT = 'NICOBAR';
      Result: [(92.6,)]
      Response: The total current groundwater extraction for the NICOBAR district is 92.6 ham.

    **Your Turn:**

    - Question: {question}
      SQL query: {query}
      Result: {result}
      Response:
    """
    
    prompt2 = ChatPromptTemplate.from_template(template2)
    chain2 = prompt2 | llm
    response = chain2.invoke({"question": question, "query": query, "result": result, "schema": get_database_schema()})
    return response.content.strip()

# --- 4. Streamlit Application UI ---
st.set_page_config(page_icon="💧", page_title="Chat with Groundwater Data", layout="centered")
st.title("💧 Chat with Groundwater Database")

if "chat" not in st.session_state:
    st.session_state.chat = [{"role": "assistant", "content": "Hello! Please connect to the database using the sidebar to get started."}]

for message in st.session_state.chat:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if user_question := st.chat_input('Ask a question about your data...'):
    if "db" not in st.session_state or not st.session_state.db:
        st.error('Please connect to a database first using the sidebar.')
    else:
        st.session_state.chat.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                sql_query = get_query_from_llm(user_question)
                
                with st.expander("Generated SQL Query"):
                    st.code(sql_query, language="sql")
                
                query_result = run_query(sql_query)
                final_response = get_response_for_query_result(user_question, sql_query, query_result)
                st.markdown(final_response)
        
        st.session_state.chat.append({"role": "assistant", "content": final_response})

# --- 5. Sidebar for Connection ---
with st.sidebar:
    st.title('🗄️ Database Connection')
    st.write("Connect to your local SQLite file.")
    
    db_filename = st.text_input(label="Database File", key="db_file", value="groundwater_from_sql.db")

    if st.button("Connect"):
        with st.spinner("Connecting..."):
            db_connection = connect_database(db_file_path=db_filename)
            if db_connection:
                st.session_state.db = db_connection
                st.success("Connection successful!")
                st.session_state.chat.append({"role": "assistant", "content": f"Successfully connected to `{db_filename}`. You can now ask questions."})
                st.rerun()