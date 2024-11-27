import streamlit as st

# Set the title of the app
st.title("Streamlit Code Execution App")

# Add a description
st.write("Click the button below to execute and test the code!")

# Create a button-styled link using st.markdown
st.markdown(
    """
    <style>
    .blue-button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        text-align: center;
        display: inline-block;
        text-decoration: none;
    }
    .blue-button:hover {
        background-color: #0056b3;
    }
    </style>
    <a href="https://code-execution-modul-compiler-sairam-project1.streamlit.app/" target="_blank" class="blue-button">Code Execution and Testing</a>
    """,
    unsafe_allow_html=True
)
