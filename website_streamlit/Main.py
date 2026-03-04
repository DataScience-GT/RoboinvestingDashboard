import streamlit as st
from pages import Home, Login, Chatbot, Learn, Assets

st.set_page_config(page_title="RoboInvesting", page_icon="📈", layout="wide")

hide_streamlit_style = """
            <style>
            /* Hide the default Streamlit top menu and footer */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Completely hide the sidebar container and the toggle button */
            [data-testid="stSidebar"] {display: none;}
            [data-testid="stSidebarCollapsedControl"] {display: none;}

            /* ChatGPT-inspired dark theme with gradient */
            .stApp {
                background: linear-gradient(180deg, #1a1a2e 0%, #0d1117 50%, #000000 100%) !important;
                background-attachment: fixed !important;
            }
            
            h1, h2, h3, h4, h5, h6 { color: #f5f5f5 !important; }
            p { color: #d4d4d8 !important; }
            
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

            /* Tab Styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 20px;
                background-color: transparent;
            }
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                background-color: transparent;
                color: #d4d4d8 !important;
            }
            .stTabs [aria-selected="true"] {
                color: #f5f5f5 !important;
                border-bottom: 2px solid #8b5cf6 !important;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #8b5cf6;'>📈 RoboInvesting</h1>", unsafe_allow_html=True)

PAGES = {
    "Home": Home,
    "Login": Login,
    "Chatbot": Chatbot,
    "Learn": Learn,
    "Assets": Assets
}

tabs = st.tabs(list(PAGES.keys()))

for i, tab_name in enumerate(PAGES.keys()):
    with tabs[i]:
        PAGES[tab_name].app()








