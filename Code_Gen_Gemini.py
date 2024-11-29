import os
import streamlit as st
import google.generativeai as genai

# Hide Streamlit menu bar, footer, and GitHub links
hide_menu_and_footer = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
a[href*="github.com"] {display: none;}
</style>
"""
st.markdown(hide_menu_and_footer, unsafe_allow_html=True)

# Configure Google Generative AI with the provided API key
GOOGLE_API_KEY = "AIzaSyBm6NVne2mZpyc6abAACbKWnAcmlZ_FWbY"  # Replace with your actual API key
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"Failed to configure Google Generative AI: {e}")
    st.stop()

# Fetch available models that support "generateContent"
available_models = []
try:
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods and "1.5" in m.name:
            available_models.append(m.name)

    if not available_models:
        st.error("No suitable models found that support content generation with version 1.5.")
        st.stop()
except Exception as e:
    st.error(f"Error fetching models: {e}")
    st.stop()

# Use the first available model
model_name = available_models[0]
try:
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat(history=[])
except Exception as e:
    st.error(f"Failed to initialize chat with model '{model_name}': {e}")
    st.stop()

# Streamlit UI
st.title("💻 LLM-Based Code Assistant")
st.write("Generate Python code snippets with varying complexity, complete with explanations and complexity analysis.")

# Input for user prompt
user_prompt = st.text_input("Enter your code request:", placeholder="e.g., Generate Python code for sorting algorithms.")

# Text area for extra details
extra_details = st.text_area(
    "Additional Details (e.g., constraints, test cases):",
    placeholder="Provide more context if needed (optional).",
    height=200,
)

# Submit button to get response
if st.button("Generate"):
    if user_prompt:
        # Show a loading spinner while fetching the response
        with st.spinner("Generating code, please wait..."):
            try:
                # Construct the prompt
                prompt = (
                    f"Generate 3 Python codes with different levels of complexity (basic, intermediate, and advanced) "
                    f"for the following request. Include comments in the code and display time and space complexity. "
                    f"Provide the code in separate boxes with a 'Copy' button for each snippet:\n\n"
                    f"Request: {user_prompt}\n\n"
                    f"Additional Details: {extra_details}"
                )

                # Send the request to the model
                response = chat.send_message(prompt, stream=True)
                output = ""

                for chunk in response:
                    if chunk.text:
                        output += chunk.text

                # Split the response into individual code blocks and display them with a "Copy" button
                st.markdown("### Generated Code Snippets:")
                code_blocks = output.split("```")
                for i, block in enumerate(code_blocks):
                    if block.strip():
                        st.code(block.strip(), language="python")
                        st.button("Copy Code", key=f"copy_button_{i}")

            except Exception as e:
                # Handle errors during generation
                st.error(f"An error occurred while generating code: {e}")
    else:
        st.warning("Please enter a code request before clicking 'Generate'.")

# Footer
st.markdown("<br><hr><small>Powered by Google Generative AI</small>", unsafe_allow_html=True)

