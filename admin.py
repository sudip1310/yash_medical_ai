import streamlit as st
from PIL import Image

def admin_page():
    st.title("Admin Page")

    st.write("")
    st.write("")
    st.write("")

    with st.container():
        with st.expander(" Send Reminder for Appointment"):
            exp1=Image.open("images/exp1_2.png")
            st.image(exp1,use_column_width=True)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        
        with st.expander(" Edit the notification message"):
            st.write("")
            # exp1=Image.open("images\exp1.png")
            # st.image(exp1,use_column_width=True)
