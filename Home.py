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
    "[**Knowledge Extractor**](http://localhost:8501)"
)

# Add a button for Code Generation with Gemini that redirects to the specified URL


st.markdown(
    "[**Code Generation With Gemini**](https://code-gen-gemini-sairam-project1.streamlit.app/)"
)
# Footer
st.write("---")
st.write("Created by Sairam - Project 1")
