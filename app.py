import streamlit as st

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import LLMChain

from prompt import system_prompt


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Career & Job Matching Assistant",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# HEADER - INNOMATICS LOGO + TITLE
# =========================================================

logo_col, title_col = st.columns([1, 5])

with logo_col:
    st.image(
    "assets/logo.webp",
    width=150
)

with title_col:
    st.markdown(
        """
        <h1 style="margin-bottom: 5px;">
            🤖 AI Career & Job Matching Assistant
        </h1>

        <p style="font-size: 16px; color: #666;">
            Your AI assistant for career guidance, job matching
            and interview preparation.
        </p>
        """,
        unsafe_allow_html=True
    )


st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Assistant")

    st.write(
        """
        This AI assistant can help you with:

        • Career guidance  
        • Job description analysis  
        • Resume improvement  
        • Skill-gap analysis  
        • Interview preparation  
        • Learning roadmaps
        """
    )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.session_state.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )

        st.rerun()


# =========================================================
# LLM
# =========================================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)


# =========================================================
# MEMORY
# =========================================================

if "memory" not in st.session_state:

    st.session_state.memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True
    )


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),

        MessagesPlaceholder(
            variable_name="history"
        ),

        ("human", "{query}")
    ]
)


# =========================================================
# CHATBOT
# =========================================================

chatbot = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=st.session_state.memory
)


# =========================================================
# CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# USER INPUT
# =========================================================

question = st.chat_input(
    "Ask me about careers, jobs, skills or interviews..."
)


# =========================================================
# RESPONSE
# =========================================================

if question:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)


    # AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = chatbot.invoke(
                {
                    "query": question
                }
            )

            answer = response["text"]

            st.markdown(answer)


    # Save response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )