import streamlit as st
from db_c import conn,cursor
st.title("media platform")
Login,Signup =st.tabs(["Login","Signup"])
with Signup:
    with st.form("Signup form"):
        st.header("Signup form")
        name=st.text_input("Name")
        email=st.text_input("Email")
        password=st.text_input("password",type="password")
        btn=st.form_submit_button("Signup")

with Login:
    with st.form("Login form"):
        st.header("Login form")
        email=st.text_input("Email")
        password=st.text_input("password",type="password")
        btn=st.form_submit_button("Login")



