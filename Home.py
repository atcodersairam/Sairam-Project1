import streamlit as st
import webbrowser

# Set the title of the app
st.title("Streamlit Code Execution App")

# Add a description
st.write("Click the button below to execute and test the code!")

# Create the button
if st.button("Code Execution and Testing"):
    # Redirect to the provided URL when the button is clicked
    webbrowser.open("https://code-execution-modul-compiler-sairam-project1.streamlit.app/")
