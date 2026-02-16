import streamlit as st
import requests
import time

def app():
    BACKEND_URL = "http://localhost:8080/api/chat"
    
    # Initialize conversation history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Add custom styling for ChatGPT-like interface
    st.markdown("""
    <style>
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        padding: 1rem 1.5rem !important;
        width: 100% !important;
    }
    h1 {
        text-align: center !important;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .user-message {
        background-color: #262626;
        justify-content: flex-end;
    }
    .assistant-message {
        background-color: #1a1a2e;
        justify-content: flex-start;
    }
    /* Style chat message avatars - white icons on purple background */
    [data-testid="stChatMessageAvatar"],
    div[data-testid="stChatMessage"] > div:first-child,
    .stChatMessage > div:first-child {
        background-color: #8b5cf6 !important;
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
        color: white !important;
        border-radius: 50% !important;
    }
    
    /* Style all SVG icons inside avatars to be white */
    [data-testid="stChatMessageAvatar"] svg,
    [data-testid="stChatMessageAvatar"] path,
    div[data-testid="stChatMessage"] > div:first-child svg,
    div[data-testid="stChatMessage"] > div:first-child path,
    .stChatMessage > div:first-child svg,
    .stChatMessage > div:first-child path {
        color: white !important;
        fill: white !important;
        stroke: white !important;
    }
    
    /* Target user message avatar specifically */
    div[data-testid="stChatMessage"][data-message-role="user"] > div:first-child,
    div[data-testid="stChatMessage"][data-message-role="user"] [data-testid="stChatMessageAvatar"] {
        background-color: #8b5cf6 !important;
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
    }
    
    /* Target assistant message avatar specifically */
    div[data-testid="stChatMessage"][data-message-role="assistant"] > div:first-child,
    div[data-testid="stChatMessage"][data-message-role="assistant"] [data-testid="stChatMessageAvatar"] {
        background-color: #8b5cf6 !important;
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
    }
    
    /* Override any default Streamlit avatar colors - comprehensive targeting */
    [data-testid="stChatMessageAvatar"] *,
    [data-testid="stChatMessage"] > div:first-child * {
        color: white !important;
    }
    
    /* Target the avatar circle/container directly - this is the key selector */
    [data-testid="stChatMessage"] > div:first-child,
    [data-testid="stChatMessageAvatar"] {
        background: #8b5cf6 !important;
        background-color: #8b5cf6 !important;
        background-image: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
    }
    
    /* Force all SVG content to be white */
    [data-testid="stChatMessage"] svg,
    [data-testid="stChatMessageAvatar"] svg {
        color: white !important;
    }
    
    [data-testid="stChatMessage"] svg path,
    [data-testid="stChatMessageAvatar"] svg path,
    [data-testid="stChatMessage"] svg circle,
    [data-testid="stChatMessageAvatar"] svg circle,
    [data-testid="stChatMessage"] svg rect,
    [data-testid="stChatMessageAvatar"] svg rect {
        fill: white !important;
        stroke: white !important;
        color: white !important;
    }
    
    /* Override inline styles that Streamlit might apply */
    [data-testid="stChatMessage"] > div:first-child[style*="background"],
    [data-testid="stChatMessageAvatar"][style*="background"] {
        background: #8b5cf6 !important;
        background-color: #8b5cf6 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)
    
    st.title("RoboInvesting Chatbot")
    
    # Display conversation history
    chat_container = st.container()
    with chat_container:
        if st.session_state.messages:
            for message in st.session_state.messages:
                role = message["role"]
                content = message["content"]
                
                if role == "user":
                    with st.chat_message("user"):
                        st.write(content)
                else:
                    with st.chat_message("assistant"):
                        st.write(content)
        else:
            st.info("👋 Hi! I'm your RoboInvesting assistant. Ask me anything about finance and investments!")
    
    # Input area at the bottom
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create a form for the input to handle Enter key
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                label="", 
                placeholder="Ask anything about finance and investments...",
                label_visibility="collapsed",
                key="user_input"
            )
        with col2:
            submit_button = st.form_submit_button("Send", use_container_width=True)
    
    # Clear chat button
    if st.session_state.messages:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Handle message submission
    if submit_button and user_input.strip():
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show user message immediately
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get response from backend
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        BACKEND_URL, 
                        json={"message": user_input},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        reply = data.get("reply", "No reply received.")
                        st.write(reply)
                        # Add assistant message to history
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    else:
                        error_msg = f"Backend error (Status {response.status_code}): {response.text}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        
                except requests.exceptions.ConnectionError:
                    error_msg = "❌ Cannot connect to backend server. Please make sure the backend server is running on port 8080."
                    st.error(error_msg)
                    st.info("💡 To start the backend server, run: `python backend_server.py` in the website_streamlit directory")
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                except requests.exceptions.Timeout:
                    error_msg = "⏱️ Request timed out. Please try again."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        st.rerun()
    elif submit_button:
        st.warning("Please enter a message.")

