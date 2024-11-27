import os
import time
import streamlit as st
import google.generativeai as genai
import traceback
import subprocess
import sys

GOOGLE_API_KEY = "AIzaSyBm6NVne2mZpyc6abAACbKWnAcmlZ_FWbY"
genai.configure(api_key=GOOGLE_API_KEY)

available_models = []
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)

    if not available_models:
        st.error("No suitable models found that support content generation.")
        st.stop()
except Exception as e:
    st.error(f"Error fetching models: {e}")
    st.stop()

# Update to use the 'models/gemini-1.5-flash' model
model_name = "models/gemini-1.5-flash"
model = genai.GenerativeModel(model_name)
chat = model.start_chat(history=[])

st.markdown("""
    <style>
        body {
            background-color: #ADD8E6;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Ranked-Codes / Time-Complexity")
st.write("Enter 3 different Python code snippets. The system will analyze and rank them based on execution time, space complexity, and runtime success.")

user_code_1 = st.text_area("Code Snippet 1 (Python):", height=200)
user_code_2 = st.text_area("Code Snippet 2 (Python):", height=200)
user_code_3 = st.text_area("Code Snippet 3 (Python):", height=200)

def execute_code_in_subprocess(code):
    try:
        with open("temp_code.py", "w") as f:
            f.write(code)
        
        start_time = time.time()
        result = subprocess.run([sys.executable, "temp_code.py"], capture_output=True, text=True, timeout=10)
        end_time = time.time()
        
        execution_time = end_time - start_time
        if result.returncode == 0:
            return True, execution_time, result.stdout
        else:
            return False, execution_time, result.stderr
    except Exception as e:
        return False, None, str(e)

def get_complexity_from_gemini(code):
    prompt = f"Analyze the following Python code.With Each Function Name  Provide the time complexity, space complexity, and any issues that may cause failure:\n\n{code}\n\nAnswer in the format:\n- Time Complexity: O(...)\n- Space Complexity: O(...)\n- Success or Failure: (mention if there is a runtime error)\n- Improvement: O(...)"
    
    try:
        response = chat.send_message(prompt, stream=False)
        return response.text
    except Exception as e:
        return f"Error while querying Gemini: {str(e)}"

def rank_code_snippets(codes):
    results = []
    for code in codes:
        success, execution_time, error_message = execute_code_in_subprocess(code)
        complexity_info = get_complexity_from_gemini(code)
        
        if execution_time is None:
            execution_time = float('inf')
        
        results.append({
            "success": success,
            "execution_time": execution_time,
            "complexity_info": complexity_info,
            "error_message": error_message
        })
    
    results.sort(key=lambda x: (x["execution_time"], not x["success"]))
    
    return results

if st.button("Submit"):
    if user_code_1 and user_code_2 and user_code_3:
        with st.spinner("Analyzing..."):
            try:
                codes = [user_code_1, user_code_2, user_code_3]

                ranked_results = rank_code_snippets(codes)
                
                for idx, result in enumerate(ranked_results):
                    if result["success"]:
                        st.success(f"Code Snippet {idx+1} executed successfully in {result['execution_time']:.5f} seconds.")
                    else:
                        st.error(f"Code Snippet {idx+1} execution failed: {result['error_message']}")
                    
                    st.write(f"### Time and Space Complexity Analysis for Code Snippet {idx+1}:")
                    st.write(result["complexity_info"])
                    st.write("---")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
    else:
        st.warning("Please enter all three code snippets before submitting.")
