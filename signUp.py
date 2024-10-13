import streamlit as st
import pandas as pd

# Set up the page configuration
st.set_page_config(page_title="E-Commerce Sign Up", page_icon="🛒")

# CSS styles
st.markdown("""
    <style>
        .signup-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #f9f9f9;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Title of the sign-up page
st.markdown('<div class="signup-container">', unsafe_allow_html=True)
st.title("Sign Up")
st.subheader("Create an Account")

# User Input Form
with st.form("signup_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    address = st.text_area("Address")
    phone = st.text_input("Phone Number")
    terms_agreement = st.checkbox("I agree to the Terms and Conditions")
    
    # Submit button
    submit = st.form_submit_button("Sign Up")
    
    # Form validation
    if submit:
        if not username or not email or not password or not confirm_password:
            st.warning("Please fill in all required fields.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        elif not terms_agreement:
            st.error("You must agree to the Terms and Conditions to sign up.")
        else:
            # Save data to CSV
            user_data = {"Username": [username], "Email": [email], "Address": [address], "Phone": [phone]}
            df = pd.DataFrame(user_data)
            df.to_csv("user_data.csv", mode="a", header=False, index=False)

            # Display success message and redirect to main page
            st.success(f"Account created successfully! Welcome to the platform, {username}. Redirecting to the main page...")
            st.session_state.page = "main"
            st.experimental_rerun()  # Navigate back to main page

st.markdown('</div>', unsafe_allow_html=True)
