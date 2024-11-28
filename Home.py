import streamlit as st

# Set the page title
st.set_page_config(page_title="Home Page - Knowledgeable Extractor", layout="centered")

# Page content
st.title("Home")

# Add the first hyperlink (external URL)
st.markdown(
    "[**Code Execution and Testing**](https://code-execution-modul-compiler-sairam-project1.streamlit.app/)"
)

# Add another hyperlink with the updated label "Efficiency Analysis"
st.markdown(
    "[**Efficiency Analysis**](https://efficiency-analysis-sairam-project1.streamlit.app/)"
)

# Add a button for Code Generation with Gemini that redirects to the specified URL
st.markdown(
    "[**Code Generation With Gemini**](https://code-gen-gemini-sairam-project1.streamlit.app/)"
)

# Add the URL for "Know Knowledge Extractor"
st.markdown(
    "[**Knowledge Extractor**](http://localhost:8501/)"
)

# Footer
st.write("---")
st.write("Created by Sairam - Project 1")
