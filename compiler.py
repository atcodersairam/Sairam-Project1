import streamlit as st
import subprocess

# Set page layout to wide mode (Constant time and space complexity O(1))
st.set_page_config(layout="wide")

# Custom CSS for the colors you requested (Constant time and space complexity O(1))
st.markdown("""
    <style>
    .title {
        font-size: 48px;
        font-weight: bold;
        color: #800080;  /* Normal purple color */
    }
    .editor-header {
        font-size: 24px;
        font-weight: bold;
        color: #1E90FF;  /* Light blue color */
    }
    .output-header {
        font-size: 24px;
        font-weight: bold;
        color: #B76E79;  /* Rose gold color */
    }
    .stButton > button {
        background-color: #FF0000; /* Red color for Run Code button */
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stButton > button:hover {
        background-color: #e60000;  /* Darker red on hover */
    }
    .redirect-button {
        display: inline-block;
        text-align: center;
        text-decoration: none;
        background-color: #1E90FF; /* Light blue color */
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        margin-top: 20px;
    }
    .redirect-button:hover {
        background-color: #1565c0;  /* Darker blue on hover */
    }
    </style>
""", unsafe_allow_html=True)

# Applying the custom styles to different sections (Constant time and space complexity O(1))
st.markdown('<p class="title">Python Code Compiler</p>', unsafe_allow_html=True)

# Create two columns: one for the code input and one for the output (Constant time and space complexity O(1))
col1, col2 = st.columns(2)

# Input field to accept Python code from the user (Linear complexity based on input size n)
with col1:
    st.markdown('<p class="editor-header">Code Editor</p>', unsafe_allow_html=True)
    code = st.text_area("Enter Python code here:", height=300)

# Button to run the code and display the output in the second column
with col2:
    st.markdown('<p class="output-header">Output</p>', unsafe_allow_html=True)

    if st.button("Run Code"):
        if code:
            try:
                # Save the user input code to a temporary file (Time complexity O(n), Space complexity O(n))
                with open("temp_code.py", "w") as file:
                    file.write(code)
                
                # Run the Python code and capture the output or errors
                result = subprocess.run(
                    ["python", "temp_code.py"], capture_output=True, text=True
                )
                
                # Display output or errors in Streamlit
                if result.returncode == 0:
                    # If the code runs successfully, display the output (Time and space complexity O(m), where m is output size)
                    st.success("Code ran successfully!")
                    st.text("Output:\n" + result.stdout)
                else:
                    # If the code fails, display the error message (Time and space complexity O(m))
                    st.error("Code failed with the following error:")
                    st.text(result.stderr)
            
            except Exception as e:
                # Handle any unexpected errors (Constant time and space complexity O(1))
                st.error(f"An error occurred: {e}")
        else:
            # If no code was provided, prompt the user to enter some code (Constant time and space complexity O(1))
            st.warning("Please enter some code to run.")  

# Add a button for Test Case Management (Constant time and space complexity O(1))
st.markdown(
    '<a href="https://test-case-management-sairam-project1.streamlit.app/" class="redirect-button" target="_blank">Test Case Management</a>',
    unsafe_allow_html=True
)
