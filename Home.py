import streamlit as st

# Set the page title
st.set_page_config(page_title="Home Page - Code Execution and Testing", layout="centered")

# Page content
st.title("Welcome to Code Execution and Testing")

st.markdown(
    """
    This application allows you to test and execute code in a user-friendly environment.
    \n\n
    Click the link below to access the module:
    """
)

# Add the hyperlink correctly using markdown
st.markdown(
    "[**Code Execution and Testing**](https://code-execution-modul-compiler-sairam-project1.streamlit.app/)"
)

# Footer
st.write("---")
st.write("Created by Sairam - Project 1")
