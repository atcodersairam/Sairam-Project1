import streamlit as st

# Set the page title
st.set_page_config(page_title="Home Page - Knowledgeable Extractor", layout="centered")

# Page content
st.title("Home")

# Add the first hyperlink (external URL)
st.markdown(
    "[**Code Execution and Testing**](https://code-execution-modul-compiler-sairam-project1.streamlit.app/)"
)

# Add another hyperlink that redirects to the local host (port 8501)
st.markdown(
    "[**Local Streamlit App (Port 8501)**](http://localhost:8501)"
)

# Footer
st.write("---")
st.write("Created by Sairam - Project 1")
