import streamlit as st

# Hyperlink that triggers a redirect
url = "https://code-execution-modul-compiler-sairam-project1.streamlit.app/"
st.markdown('[Code Execution and Testing](#)', unsafe_allow_html=True)

# Redirect the user to the URL when they click the link
if st.button('Code Execution and Testing'):
    st.experimental_redirect(url)
