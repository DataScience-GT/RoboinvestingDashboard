import streamlit as st
import re
import hashlib

class LoginPage:
    def __init__(self):
        pass

    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login_form(self):
        # Add CSS for centering content
        st.markdown("""
        <style>
        h1 {
            text-align: center !important;
        }
        .stTextInput {
            max-width: 400px;
            margin: 0 auto;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.title("🔐 Secure Login")
        
        # Center the form inputs
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            email = st.text_input("Email Address", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_btn = st.button("Log In", use_container_width=True)
            
            if login_btn:
                if not email or not password:
                    st.error("Please fill in all fields")
                    return False

                if not self.validate_email(email):
                    st.error("Invalid email format")
                    return False

                if len(password) < 8:
                    st.error("Password must be at least 8 characters")
                    return False

                hashed_password = self.hash_password(password)
                st.success("Login Successful!")
                return True

        return False

    def run(self):
        self.login_form()


def app():
    login_page = LoginPage()
    login_page.run()
