import streamlit as st

# Set the title of the page
st.title("Streamlit Application Home Page")

# Add a description of what the page is about
st.write("""
Welcome to the Streamlit Application. 
Click any of the buttons below to perform the respective actions.
""")

# Custom CSS to style all the buttons as blue
st.markdown("""
    <style>
        .stButton>button {
            background-color: #007bff;  /* Blue background */
            color: white;               /* White text */
            border: none;               /* No border */
            border-radius: 5px;         /* Rounded corners */
            padding: 10px 20px;         /* Padding around the text */
            font-size: 16px;            /* Font size */
            cursor: pointer;           /* Pointer cursor on hover */
        }
        .stButton>button:hover {
            background-color: #0056b3;  /* Darker blue when hovered */
        }
    </style>
""", unsafe_allow_html=True)

# Create the five buttons
button_1 = st.button("Code Execution and Testing")
button_2 = st.button("Code Optimization")
button_3 = st.button("Code Generation (T5)")
button_4 = st.button("Knowledge Integration")
button_5 = st.button("Code Generation (Gemini)")

# Handle button interactions
if button_1:
    # Provide the external URL directly
    st.markdown(
        f'<a href="https://code-execution-modul-compiler-sairam-project1.streamlit.app/" target="_self">Redirecting...</a>',
        unsafe_allow_html=True
    )
    
if button_2:
    st.write("You clicked 'Code Optimization'. You can add functionality here.")
    
if button_3:
    st.write("You clicked 'Code Generation (T5)'. You can add functionality here.")
    
if button_4:
    st.write("You clicked 'Knowledge Integration'. You can add functionality here.")
    
if button_5:
    st.write("You clicked 'Code Generation (Gemini)'. You can add functionality here.")
