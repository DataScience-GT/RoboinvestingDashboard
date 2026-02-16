import streamlit as st

st.set_page_config(page_title="RoboInvesting", page_icon="📈", layout="wide")

hide_streamlit_style = """
            <style>
            /* Hide the default Streamlit top menu */
            #MainMenu {visibility: hidden;}
            
            /* Hide the footer */
            footer {visibility: hidden;}
            
            /* Hide the Streamlit default page navigation in the sidebar */
            .css-1lcbmhc {display: none;}  /* Remove the default page selector in sidebar */
            
            /* Hide Streamlit's "Main" entry from the sidebar */
            .css-1f8f0p4 {display: none;}  /* Remove "Main" option from sidebar */
            
            /* Hide Streamlit's automatic navigation, leaving only custom dropdown */
            .css-1kyxreq {display: none;}  /* Hide the default sidebar components like pages list */
            
            /* Hide the page navigation buttons/icons */
            section[data-testid="stSidebarNav"] {display: none;}
            
            /* Hide sidebar navigation links */
            .stSidebarNav {display: none;}
            nav[data-testid="stSidebarNav"] {display: none;}
            
            /* Hide any sidebar navigation elements */
            div[data-testid="stSidebarNav"] ul {display: none;}
            ul[role="listbox"] {display: none;}
            
            /* ChatGPT-inspired dark theme with gradient */
            .main {
                background: linear-gradient(180deg, #1a1a2e 0%, #0d1117 50%, #000000 100%) !important;
                background-attachment: fixed !important;
            }
            
            .stApp {
                background: linear-gradient(180deg, #1a1a2e 0%, #0d1117 50%, #000000 100%) !important;
                background-attachment: fixed !important;
            }
            
            h1, h2, h3, h4, h5, h6 {
                color: #f5f5f5 !important;
            }
            
            p {
                color: #d4d4d8 !important;
            }
            
            /* Sidebar styling */
            .css-1d391kg {
                background-color: #171717 !important;
            }
            
            .css-17eq0hr {
                background-color: #171717 !important;
            }
            
            section[data-testid="stSidebar"] {
                background-color: #171717 !important;
            }
            
            [data-testid="stSidebar"] > div {
                background-color: #171717 !important;
            }
            
            /* Input fields */
            .stTextInput > div > div > input {
                background-color: #262626 !important;
                color: #f5f5f5 !important;
            }
            
            /* Buttons */
            .stButton > button {
                background-color: #8b5cf6 !important;
                color: white !important;
                border: none !important;
                transition: all 0.3s !important;
            }
            
            .stButton > button:hover {
                background-color: #7c3aed !important;
                transform: translateY(-1px) !important;
            }
            
            /* Selectbox styling */
            .stSelectbox > div > div > div {
                background-color: #262626 !important;
                color: #f5f5f5 !important;
            }
            
            .stSelectbox label {
                color: #d4d4d8 !important;
            }
            
            .stSelectbox > div > div > select {
                background-color: #262626 !important;
                color: #f5f5f5 !important;
            }
            
            /* Markdown text */
            .stMarkdown {
                color: #f5f5f5 !important;
            }
            
            /* Error messages */
            .stAlert {
                border-left-color: #ef4444 !important;
            }
            
            /* Success messages */
            .stSuccess {
                border-left-color: #22c55e !important;
            }
            
            /* Warning messages */
            .stWarning {
                border-left-color: #f59e0b !important;
            }
`            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

from pages import Home, Login, Chatbot, Learn, Assets

PAGES = {
    "Home": Home,
    "Login": Login,
    "Chatbot": Chatbot,
    "Learn": Learn,
    "Assets": Assets
}

st.sidebar.markdown("""
    <div style='color: #f5f5f5; font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;'>
        💬 RoboInvesting
    </div>
    <hr style='border-color: #404040; margin: 1rem 0;'>
    """, unsafe_allow_html=True)
selection = st.sidebar.selectbox("", list(PAGES.keys()))

PAGES[selection].app()











