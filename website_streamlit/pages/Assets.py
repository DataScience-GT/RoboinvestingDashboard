import streamlit as st

def app():
    # Add CSS for centering content
    st.markdown("""
    <style>
    h1 {
        text-align: center !important;
    }
    .stMarkdown {
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Investment Assets")
    st.write("Asset tracking page coming soon")
