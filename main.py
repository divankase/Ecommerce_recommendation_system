import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

def show_main_page():
    # Check if user is signed in
    if 'signed_in' not in st.session_state:
        st.session_state.signed_in = False  # Initialize the signed_in state
        st.session_state.page = "Home"  # Default to home page
        st.session_state.username = None  # Initialize username
        st.session_state.logout_flag = False  # Flag for logout
        st.session_state.recent_searches = []  # Initialize recent searches

    # Sidebar navigation
    with st.sidebar:
        selected = option_menu("Recommendation System App", ["Home", "SignIn", "SignUp", "Search Product"], 
                               icons=["house", "person", "lock", "search"], 
                               menu_icon="cast", default_index=0)

    # CSS for background image
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url("Background.jpg");  /* Replace with your image path */
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }
        .sidebar .sidebar-content {
            background-color: rgba(255, 255, 255, 0.8); /* Slightly transparent sidebar */
        }
        .logout-button {
            position: fixed;  /* Fixed positioning */
            bottom: 20px;  /* Distance from the bottom */
            right: 20px;  /* Distance from the right */
            background-color: #f44336;  /* Red background color */
            color: white;  /* White text color */
            border: none;  /* No border */
            padding: 10px 15px;  /* Padding for the button */
            border-radius: 5px;  /* Rounded corners */
            font-size: 12px;  /* Small font size */
            cursor: pointer;  /* Pointer cursor on hover */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Logout functionality
    def logout():
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.logout_flag = True  # Set logout flag

    # Check if logout flag is set to rerun the app
    if st.session_state.logout_flag:
        st.session_state.signed_in = False
        st.session_state.page = "Home"
        st.session_state.username = None
        st.session_state.recent_searches = []
        st.session_state.logout_flag = False  # Reset logout flag
        st.experimental_rerun()  # Rerun the app

    # Home page
    if selected == "Home":
        st.title("E-commerce Product Recommendation System")
        st.write("### Welcome to the E-commerce Product Recommendation System")
        st.write("""This application helps you discover products based on your preferences and browsing history. 
        Our recommendation model provides suggestions for products similar to the ones you choose, 
        making your shopping experience more personalized and enjoyable.""")
        st.video("video.mp4")

    # SignIn page
    if selected == "SignIn":
        st.title("Sign In")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Sign In"):
            # Check if user exists
            try:
                user_data = pd.read_csv('user_data.csv')
                if 'Email' in user_data.columns and 'Password' in user_data.columns:
                    if email in user_data['Email'].values:
                        user_row = user_data.loc[user_data['Email'] == email]
                        if user_row['Password'].values[0] == password:
                            st.success(f"Sign In successful! Welcome {user_row['Username'].values[0]}. You can search your recommended products now.")
                            st.session_state.signed_in = True
                            st.session_state.username = user_row['Username'].values[0]
                            st.session_state.recent_searches = user_row['Recent Searches'].dropna().tolist()  # Load recent searches
                            st.session_state.page = "Search Product"  # Redirect to Search Product page
                        else:
                            st.error("Incorrect password.")
                    else:
                        st.error("User does not exist. Please sign up.")
                else:
                    st.error("User data file is corrupted. Please reset your data.")
            except FileNotFoundError:
                st.error("User data not found. Please sign up.")

    # SignUp page
    if selected == "SignUp":
        st.title("Sign Up")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Sign Up"):
            # Check if the user already exists
            try:
                user_data = pd.read_csv('user_data.csv')
                if 'Email' in user_data.columns and 'Password' in user_data.columns:
                    if email in user_data['Email'].values:
                        st.error("Email already exists. Please sign in.")
                    else:
                        new_user = pd.DataFrame({'Username': [username], 'Email': [email], 'Password': [password], 'Recent Searches': [""]})
                        new_user.to_csv('user_data.csv', mode='a', header=False, index=False)
                        st.success("Sign Up successful! You can now sign in.")
                else:
                    st.error("User data file is corrupted. Please reset your data.")
            except FileNotFoundError:
                new_user = pd.DataFrame({'Username': [username], 'Email': [email], 'Password': [password], 'Recent Searches': [""]})
                new_user.to_csv('user_data.csv', index=False)
                st.success("Sign Up successful! You can now sign in.")

    # Search Product page
    if selected == "Search Product":
        if st.session_state.signed_in:
            # User is signed in, show the app content
            st.title("Search Product")
            
            # Show recent searches if available
            if st.session_state.recent_searches:
                st.write("### Recent Searches")
                for search in st.session_state.recent_searches:
                    st.write(f"- {search}")

            # Import and run app logic
            import app  # Import app logic
            app.run()  # Call the main function of your app logic

            # Add logout button if the user is signed in
            if st.session_state.signed_in:
                if st.button("Logout", key="logout_button", help="Click to logout", on_click=logout):
                    st.write("Logging out...")

        else:
            # User is not signed in, prompt to sign in
            st.error("You need to sign in to access the Search Product page.")

# Run the app
if __name__ == "__main__":
    show_main_page()
