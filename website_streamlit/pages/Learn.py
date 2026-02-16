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
    
    st.title("Learning Center")
    st.write("Educational resources coming soon")
