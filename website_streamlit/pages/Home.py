import streamlit as st

def app():
    # Add CSS for centering content and ChatGPT-inspired styling
    st.markdown("""
    <style>
    .main .block-container {
        max-width: 100%;
        padding-top: 2rem;
        background: transparent !important;
    }
    .centered {
        text-align: center !important;
        display: block !important;
        margin: 0 auto !important;
        color: #d4d4d8 !important;
    }
    h1.centered-title {
        text-align: center !important;
        display: block !important;
        margin: 0 auto !important;
        color: #f5f5f5 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create centered title using markdown
    st.markdown("<h1 class='centered-title'>RoboInvestor Dashboard</h1>", unsafe_allow_html=True)
    
    # Center the welcome message
    st.markdown("<p class='centered' style='font-size: 1.2em;'>Welcome to the main dashboard of the RoboInvesting Project</p>", unsafe_allow_html=True)

    st.markdown("<p class='centered' style='font-size: 1.2em;'>This is a product of the Data Science Club at Georgia Tech and is not responsible for any financial decisions you make.</p>", unsafe_allow_html=True)
