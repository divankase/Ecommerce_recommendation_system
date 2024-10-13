import streamlit as st
import pandas as pd

# CSS styles
st.markdown("""
    <style>
        /* Your CSS styles here */
        .signin-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #f9f9f9;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Title of the sign-in page
st.markdown('<div class="signin-container">', unsafe_allow_html=True)
st.title("Sign In")
st.subheader("Welcome Back!")

# User Input Form
with st.form("signin_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    # Sign In button
    submit = st.form_submit_button("Sign In")
    
    if submit:
        try:
            # Load user data
            user_data = pd.read_csv("user_data.csv", header=None, names=["Username", "Email", "Password", "Address", "Phone"])
            user = user_data[(user_data['Email'] == email) & (user_data['Password'] == password)]
            
            if not user.empty:
                st.success(f"Welcome back, {user['Username'].values[0]}!")
                st.session_state.page = "app"  # Set session state to navigate to app.py
                st.experimental_rerun()  # Rerun the app to navigate
            else:
                st.error("User does not exist. Please sign up.")
                if st.button("Sign Up"):
                    st.session_state.page = "signUp"  # Navigate to sign up
                    st.experimental_rerun()  # Rerun the app to navigate
        except FileNotFoundError:
            st.error("User data not found. Please sign up first.")
st.markdown('</div>', unsafe_allow_html=True)

