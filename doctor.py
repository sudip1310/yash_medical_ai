import streamlit as st
from PIL import Image

def doctor_page():
    st.title("Doctor Page")

    st.write("")
    st.write("")
    st.write("")

    static_doctor_content=Image.open("images/Doctor_page_static content.png")
    st.image(static_doctor_content,use_column_width=True)




