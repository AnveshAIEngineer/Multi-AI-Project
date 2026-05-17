import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Multi AI Agent",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F8FAFC;
}

/* Main container */
.main .block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Title */
.main-title {
    font-size: 52px;
    font-weight: 700;
    color: #111827;
    letter-spacing: -1px;
    margin-bottom: 0.2rem;
}

/* Subtitle */
.sub-text {
    font-size: 17px;
    color: #6B7280;
    margin-bottom: 2rem;
}

/* Cards */
.custom-card {
    background: white;
    padding: 28px;
    border-radius: 18px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    margin-bottom: 24px;
}

/* Labels */
label {
    font-weight: 600 !important;
    color: #111827 !important;
}

/* Inputs */
.stTextArea textarea {
    border-radius: 14px !important;
    border: 1px solid #D1D5DB !important;
    background-color: #FFFFFF !important;
    color: #111827 !important;
    padding: 14px !important;
    font-size: 15px !important;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px !important;
    border: 1px solid #D1D5DB !important;
    background-color: white !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

/* Button */
.stButton button {
    background-color: #111827;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.8rem 1rem;
    font-size: 15px;
    font-weight: 600;
    width: 100%;
    transition: 0.2s ease;
}

.stButton button:hover {
    background-color: #1F2937;
}

/* Response box */
.response-box {
    background: white;
    border-radius: 18px;
    padding: 28px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    margin-top: 24px;
    line-height: 1.8;
    color: #111827;
    font-size: 16px;
}

/* Remove weird top padding */
header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown(
    "<div class='main-title'>Multi AI Agent</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-text'>AI workspace powered by GROQ and Tavily Search</div>",
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## Configuration")

    selected_model = st.selectbox(
        "Select Model",
        settings.ALLOWED_MODEL_NAMES
    )

    allow_web_search = st.toggle(
        "Enable Web Search",
        value=True
    )

    st.markdown("---")

    st.caption(
        "FastAPI • Streamlit • LangChain • GROQ"
    )

# ---------------- MAIN CARD ----------------

st.markdown("<div class='custom-card'>", unsafe_allow_html=True)

system_prompt = st.text_area(
    "System Prompt",
    placeholder="Define AI role and behavior...",
    height=120
)

user_query = st.text_area(
    "User Query",
    placeholder="Ask anything...",
    height=220
)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- API ----------------

API_URL = "http://127.0.0.1:9999/chat"

# ---------------- BUTTON ----------------

if st.button("Generate Response"):

    if not user_query.strip():
        st.warning("Please enter a query.")

    else:

        payload = {
            "model_name": selected_model,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        try:

            with st.spinner("Generating response..."):

                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=120
                )

            if response.status_code == 200:

                agent_response = response.json().get(
                    "response",
                    ""
                )

                st.markdown(
                    f"""
                    <div class="response-box">
                        {agent_response}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.error("Backend error occurred.")

        except Exception as e:

            logger.error(str(e))

            st.error(
                str(
                    CustomException(
                        "Failed to communicate with backend"
                    )
                )
            )