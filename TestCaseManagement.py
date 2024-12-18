import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyAWcupp9ne56J5_hMoSmw8gRUvfPIwl0RQ"
genai.configure(api_key=GOOGLE_API_KEY)

# Fetch available models
available_models = []
try:
    for m in genai.list_models():
        # Check if 'generateContent' is supported by the model
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)

    if not available_models:
        st.error("No suitable models found that support content generation.")
        st.stop()

except Exception as e:
    st.error(f"Error fetching models: {e}")
    st.stop()

# Choose the Gemini 1.5 Flash model
model_name = "models/gemini-1.5-flash"  # Corrected to use available model name
if model_name not in available_models:
    st.error(f"The model {model_name} is not available. Please check for updates or available models.")
    st.stop()

model = genai.GenerativeModel(model_name)
chat = model.start_chat(history=[])

st.markdown("""
    <style>
        body {
            background-color: #ADD8E6;
        }
        .blue-btn {
            display: inline-block;
            background-color: #007BFF;
            color: #F1F1F1; /* Lighter white text for better contrast */
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            text-align: center;
            text-decoration: none;
            margin: 5px;
            transition: background-color 0.3s;
        }
        .blue-btn:hover {
            background-color: #0056b3; /* Darker blue on hover */
        }
        .back-btn {
            position: fixed;
            left: 20px;
            bottom: 20px;
        }
        .ranked-btn {
            position: fixed;
            right: 20px;
            bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Python Code Analyzer - Test Cases and Edge Cases")
st.write("Enter a Python code snippet to get suggested test cases and edge cases.")

user_code = st.text_area("Python Code Snippet:", height=200)

def get_test_cases_from_gemini(code):
    prompt = f"""
    Analyze the following Python code and provide a list of suggested test cases, including edge cases, if a test case is given as input, then provide changes in that code:

    Code:
    {code}
    
    Answer in the following format:
    - Suggested Test Cases: (List of test cases including edge cases)
    """

    try:
        # Send the message to Gemini and get the response
        response = chat.send_message(prompt, stream=False)
        return response.text
    except Exception as e:
        return f"Error while querying Gemini: {str(e)}"

# Button to generate test cases
if st.button("Generate Test Cases"):
    if user_code:
        with st.spinner("Generating test cases..."):
            try:
                # Get test cases from Gemini
                test_cases_result = get_test_cases_from_gemini(user_code)
                
                # Display the test cases
                st.write("### Suggested Test Cases and Edge Cases:")
                st.write(test_cases_result)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a Python code snippet before submitting.") 

# Add back and ranked code buttons with fixed positions
st.markdown(
    '<a href="https://code-execution-modul-compiler-sairam-project1.streamlit.app/" class="blue-btn back-btn" target="_blank">Compiler</a>',
    unsafe_allow_html=True
)
st.markdown(
    '<a href="https://rank-codes-sairam-project1.streamlit.app/" class="blue-btn ranked-btn" target="_blank">Ranked Code</a>',
    unsafe_allow_html=True
)
