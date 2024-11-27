import streamlit as st

# Define the URL to redirect to
url = "https://code-execution-modul-compiler-sairam-project1.streamlit.app/"

# Create a clickable button
if st.button('Code Execution and Testing'):
    st.experimental_set_query_params(redirect=url)
    st.experimental_redirect(url)
