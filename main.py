import streamlit as st
from pathlib import Path
import pickle
import streamlit_authenticator as stauth
import os
from streamlit_option_menu import option_menu
from admin import admin_page
from doctor import doctor_page
from member import member_page
from PIL import Image

# get user information
user_info = {}
cred_path = Path(__file__).parent / "hashed_passwords.pkl"
with cred_path.open("rb") as file:
    user_info = pickle.load(file)
    
credentials = {
    "usernames":{
        user_info["usernames"][0] : {
            "name" : user_info["names"][0],
            "password" : user_info["passwords"][0]
            }         
        }
}

# get the list of pdf files
file_directory = os.path.join(Path.cwd(),"file_directory")
pdf_files = [f'sample{i}.pdf' for i in range(1, len(os.listdir(file_directory))+1)]

cookie_name = "sample_app"
authenticator = stauth.Authenticate(credentials, cookie_name, "abcd", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

def logout():
    authenticator.cookie_manager.delete(cookie_name)
    st.session_state['logout'] = True
    st.session_state['name'] = None
    st.session_state['username'] = None
    st.session_state['authentication_status'] = None

if authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
    
if authentication_status:
    logo_img = Image.open('images/resoluteai_logo.webp')
    st.sidebar.image(logo_img)
    
    st.markdown(
        """
        <style>
            .css-1544g2n {
                padding: 0.5rem 0.5rem 0.5rem;
            }
        </style>
        """,
            unsafe_allow_html=True,
        )
    
    st.markdown(
        """
        <style>
            .css-1y4p8pa {
                padding-top: 0rem;
                max-width: 50rem;
            }
        </style>
        """,
            unsafe_allow_html=True,
        )
    
    with st.sidebar:
        selected_page = option_menu(
            menu_title=None,
            options = ["Admin", "Doctor", "Member", "Logout"],
            icons = ["gear", "clipboard-pulse", "person", "box-arrow-left"]
        )
    
    if selected_page == "Admin":
        admin_page()
    if selected_page == "Doctor":
        doctor_page()
    if selected_page == "Member":
        member_page()
    if selected_page == "Logout":
        logout()
    #=======================================
