import streamlit as st

if "is_adimin" not in st.session_state:
    st.session_state.is_admin = False

st.header("Admin Page")

name = st.text_input("Enter your name:")

if name:
    st.write(f"Hello, {name}!")
    st.session_state.is_admin = True

print("is_admin:", st.session_state.is_admin)
