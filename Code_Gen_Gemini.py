import os
import re
import streamlit as st
import google.generativeai as genai

# Configure Google Generative AI with the provided API key
GOOGLE_API_KEY = "AIzaSyBm6NVne2mZpyc6abAACbKWnAcmlZ_FWbY"  # Your provided API key
genai.configure(api_key=GOOGLE_API_KEY)

# List available models and find the appropriate one (e.g., version 1.5)
available_models = []
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # Look for models with version 1.5 in the model name or metadata
            if '1.5' in m.name:
                available_models.append(m.name)

    # Check if we have available models
    if not available_models:
        st.error("No suitable models found that support content generation with version 1.5.")
        st.stop()
except Exception as e:
    st.error(f"Error fetching models: {e}")
    st.stop()

# Use the first available model (ensure it's version 1.5)
model_name = available_models[0]
model = genai.GenerativeModel(model_name)
chat = model.start_chat(history=[])

# Streamlit UI
st.title("LLM-Based-CODE-ASSIST")
st.write("Code-Generator")

# Input for user prompt using a text input box
user_prompt = st.text_input("Request-Drop Box:")

# Input for extra details using a longer text area for additional context or instructions
extra_details = st.text_area("Test-Cases-Constraints-Extra-Details:", height=200)

# Submit button to get response
if st.button("Generate"):
    if user_prompt:
        if user_prompt.lower() == "exit":
            st.write("Session ended.")
        else:
            # Show a loading spinner while fetching the response
            with st.spinner("Loading..."):
                try:
                    # Combine the user prompt and additional details
                    prompt = (
                        f"Generate 3 Python codes with different complexity in time and space,  comments,in seperate box with copy button for each code "
                        f"in readable colored lines, hardcoded input, readily executable code with time complexity "
                        f"of each code:\n"
                        f"{user_prompt}\n{extra_details}"
                    )
                    response = chat.send_message(prompt, stream=True)

                    output = ""
                    for chunk in response:
                        if chunk.text:
                            output += chunk.text

                    # Display the output as plain text without code block markers
                    st.markdown(output)  # Display the output in markdown format

                except Exception as e:
                    # Handle specific errors related to the model's response
                    if "Invalid operation" in str(e):
                        st.error("The response did not contain valid text. Please try rephrasing your question.")
                    elif "unexpected model name format" in str(e):
                        st.error("The selected model name is not recognized. Please check the available models.")
                    else:
                        st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a request before submitting.")
