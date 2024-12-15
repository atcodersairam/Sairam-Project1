import streamlit as st
import google.generativeai as genai
import time

# Hardcoded API key (not recommended for production)
GOOGLE_API_KEY = "AIzaSyDbufXAwGsoQ6WrR0YcW3F7rlGVOgd-igE"
genai.configure(api_key=GOOGLE_API_KEY)

# Streamlit UI Setup
st.title("Gemini AI Code Generation (1.5 Model)")
st.write("Enter a prompt to generate code suggestions using Gemini AI 1.5.")

# Input from the user
user_input = st.text_area("Enter your prompt here:", height=300)

# Define how to structure content for generating code based on ideas
def generate_code_prompt(user_input):
    # This function will format the user input to make it clear we're asking for code
    prompt = f"""
    You are a powerful AI that helps generate Python code based on user ideas. 

    The user has a project idea and needs Python code for it. 
    Please generate Python code that solves the following problem:

    "{user_input}"

    The generated code should be clean, efficient, and well-commented, following best coding practices.

    Please include all necessary imports, code structure, and comments for clarity.

    If there are multiple ways to solve this problem, suggest one efficient approach with an explanation.
    """
    return prompt

# Function to list and select the appropriate model
def select_model():
    try:
        models = [
            m.name for m in genai.list_models()
            if 'generateContent' in m.supported_generation_methods
        ]
        for model in models:
            if "gemini-1.5-flash" in model:
                return model
        st.error("Gemini 1.5 model not found among available models.")
        st.stop()
    except Exception as e:
        st.error(f"Error fetching models: {e}")
        st.stop()

# Get the Gemini 1.5 model
model_name = select_model()
model = genai.GenerativeModel(model_name)
chat = model.start_chat(history=[])

# Submit and generate
if st.button("Generate Code"):
    if user_input:
        # Generate a well-structured prompt
        prompt = generate_code_prompt(user_input)

        # Generate response using Gemini
        with st.spinner("Generating code..."):
            start_time = time.time()
            try:
                response = chat.send_message(prompt, stream=True)
                suggestions = []
                output = ""
                for chunk in response:
                    if chunk.text:
                        output += chunk.text
                        suggestions.append(chunk.text)

                # Calculate execution time
                execution_time = time.time() - start_time

                # Display suggestions
                st.success(f"Code generation completed in {execution_time:.2f} seconds.")
                st.write("Code Suggestions:")
                for idx, suggestion in enumerate(suggestions, 1):
                    st.markdown(f"**Suggestion {idx}:**")
                    st.code(suggestion)
            except Exception as e:
                st.error(f"An error occurred while generating code: {e}")
    else:
        st.warning("Please enter a prompt before generating.")
