import streamlit as st
import os
import yaml
from streamlit_authenticator import Authenticate
from authenticate_files.validator import Validator
from authenticate_files.utils import generate_random_pw
from session_state import SessionState
import uuid
from authenticate_files.hasher import Hasher

# Function to generate unique key
def generate_key():
    return str(uuid.uuid4())

# Load configuration from YAML file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

# Set the favicon
st.set_page_config(page_title="IDG Customer Churn Predictor App", page_icon="🏠")

# Initialize session state
session_state = SessionState(authenticated=False, form_state={
    "username": "shantanu",
    "password": "shantanu@123",
    "new_username": "shantanu",
    "new_password": "shantanu@123",
    "confirm_password": "shantanu@123"
})

# Home page function
@st.cache_resource
def home_page():
    image_filename = "home.png"
    home_image_path = os.path.join("images", image_filename)
    st.image(home_image_path, use_column_width=True)

    st.markdown("## **This is a Streamlit app for predicting churn.**")
    st.write("**Features:**")
    st.write("- Predict customer churn based on various features.")
    st.write("- Allow users to log in and create accounts.")
    st.write("- Provide interactive visualizations of churn prediction results.")
    st.write("**Benefits:**")
    st.write("- Helps businesses identify customers at risk of churning.")
    st.write("- Enables proactive retention strategies to reduce churn.")
    st.write("- Streamlines the churn prediction process with a user-friendly interface.")
    st.write("**Machine Learning Integrations:**")
    st.write("- Utilizes machine learning models for churn prediction.")
    st.write("- Supports algorithms like Random Forest, XGBoost, and SVM.")

# Logout function
def logout():
    session_state.authenticated = False

# Login function
@st.cache_data
def login():
    username = session_state.form_state["username"]
    password = session_state.form_state["password"]
    authenticator = Authenticate(config['credentials'], config['cookie']['name'], config['cookie']['key'], config['cookie']['expiry_days'], config['preauthorized'])

    try:
        auth_result = authenticator.login(username, password)
        if auth_result[1]:
            session_state.authenticated = True
        else:
            st.error("Login failed: Incorrect username or password.")
    except Exception as e:
        st.error(f"Login failed: {str(e)}")

# Create Account function
@st.cache_data
def create_account():
    validator = Validator()
    new_username = session_state.form_state["new_username"]
    new_password = session_state.form_state["new_password"]
    confirm_password = session_state.form_state["confirm_password"]
    if not validator.validate_username(new_username):
        st.error("Invalid username format. Please use only alphanumeric characters, underscores, and hyphens.")
    elif new_password != confirm_password:
        st.error("Passwords do not match.")
    else:
        # Create a Hasher instance with the new password
        hasher = Hasher([new_password])
        # Generate the hashed password
        hashed_password = hasher.generate()[0]
        # Create the new account with the hashed password
        authenticator = Authenticate(config['credentials'], config['cookie']['name'], config['cookie']['key'], config['cookie']['expiry_days'], config['preauthorized'])
        authenticator.create_account(new_username, hashed_password)
        st.success("Account created successfully. You can now log in.")

# Main function
def main():
    col1, col2, col3 = st.columns([4, 4, 6])

    with col1:
        st.title("IDG Customer Churn Predictor App")
        st.image("images/login.png", width=250)

        login_button_key = generate_key()
        login_button = st.button("Login", key=login_button_key)

        session_state.form_state["new_username"] = st.text_input("New Username", key=f"new_username_input_{generate_key()}", value=session_state.form_state["new_username"])
        session_state.form_state["new_password"] = st.text_input("New Password", type="password", key=f"new_password_input_{generate_key()}", value=session_state.form_state["new_password"])
        session_state.form_state["confirm_password"] = st.text_input("Confirm Password", type="password", key=f"confirm_password_input_{generate_key()}", value=session_state.form_state["confirm_password"])

        create_account_button_key = generate_key()
        create_account_button = st.button("Create Account", key=create_account_button_key)

        if create_account_button:
            create_account()

        if login_button:
            login()

    with col2:
        # Display the home page content
        home_page()


if __name__ == "__main__":
    main()
