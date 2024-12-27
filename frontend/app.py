import streamlit as st
import requests

st.title("Pharmacy Chatbot")
query = st.text_input("Ask the chatbot anything:")

if st.button("Submit"):
    if query:
        response = requests.post(
            "http://localhost:8000/ask",
            json={"query": query},
        )
        if response.status_code == 200:
            st.write("Response:", response.json()["response"])
        else:
            st.write("Error:", response.text)
