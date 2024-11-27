import streamlit as st

# Set the title of the app
st.title("Streamlit Code Execution App")

# Add a description
st.write("Click the button below to execute and test the code!")

# Button labeled "Code Execution and Testing"
if st.button("Code Execution and Testing"):
    # Redirect to the provided URL when clicked
    st.markdown(
        f'<a href="https://code-execution-modul-compiler-sairam-project1.streamlit.app/" target="_blank">'
        f'<button style="background-color: #007bff; color: white; border-radius: 5px; padding: 15px 30px; font-size: 18px; font-weight: bold; border: none;">'
        f'Code Execution and Testing</button></a>',
        unsafe_allow_html=True
    )
