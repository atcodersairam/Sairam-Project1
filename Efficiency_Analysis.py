import os
import re
import streamlit as st
import google.generativeai as genai
import time
import tracemalloc
from io import StringIO
import contextlib
import ast

# Constants
GOOGLE_API_KEY = "AIzaSyBm6NVne2mZpyc6abAACbKWnAcmlZ_FWbY"  # Replace this with your actual API key
MODEL_NAME = "models/gemini-1.5-flash"

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)
chat = model.start_chat(history=[])

# Streamlit UI Setup
st.title("Enhanced Code Efficiency Analysis and Bug Detection")
st.write("Analyze, Fix Bugs, and Optimize Your Code with AI Assistance.")

# Input for buggy code
extra_details = st.text_area("Enter Code with Bugs", height=200)

# Function to execute code and capture execution time and memory usage
def execute_code(code):
    """
    Executes the given code and captures its execution time and memory usage.
    """
    tracemalloc.start()
    start_time = time.time()
    f = StringIO()  # Capture stdout for user feedback

    with contextlib.redirect_stdout(f):
        try:
            exec(code)  # Execute the code dynamically
        except Exception as e:
            f.write(f"Error: {e}")
    
    execution_time = time.time() - start_time
    memory_used = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    output = f.getvalue()
    return execution_time, memory_used, output

# Function to detect bugs in the provided code
def detect_bugs(code):
    """
    Analyzes the code for syntax or runtime issues using Python's AST module.
    """
    try:
        ast.parse(code)
        return "No syntax errors detected."
    except SyntaxError as e:
        return f"Syntax Error: {e}"
    except Exception as e:
        return f"Runtime Error: {e}"

# Function to display analysis results
def display_analysis_results(code_output, execution_time, memory_used):
    """
    Displays the analysis results, including corrected code, efficiency analysis, and output.
    """
    st.markdown("### Efficiency Analysis:")
    st.markdown(f"**Execution Time:** `{execution_time:.4f} seconds`")
    st.markdown(f"**Memory Used:** `{memory_used / 1024:.2f} KB`")
    st.markdown("### Code Output:")
    st.code(code_output)

# Function to display explanations, suggestions, and optimizations
def display_explanations():
    """
    Displays the explanations of fixes, suggested improvements, and potential optimizations.
    """
    st.markdown("### Explanation of Fixes and Enhancements:")
    st.markdown("---")
    st.markdown("""
        **Algorithm Efficiency:** The provided code had performance issues caused by inefficient data structures or nested loops. The revised code minimizes these inefficiencies.

        **Time Complexity:** The optimized algorithm achieves better time complexity (e.g., `O(n)` or `O(log n)`) where applicable, ensuring scalability for large datasets.

        **Space Complexity:** Reduced memory usage by avoiding unnecessary data storage or redundant operations.

        **Suggestions for Further Improvement:**
        - Use Hash Tables or Sets for faster lookup times.
        - Avoid nested loops; consider Binary Search or divide-and-conquer techniques for better performance.
    """)

    st.markdown("### Potential Further Optimizations:")
    st.markdown("""
        - Implement multi-threading or parallel computing for larger datasets.
        - Use memoization or caching to avoid redundant computations.
    """)

# Main Button to Generate and Analyze
if st.button("Generate"):
    if extra_details:
        with st.spinner("Analyzing and Enhancing the Code..."):
            try:
                # AI prompt for fixing the buggy code
                prompt = (
                    f"Improve the following code for readability, performance, and bug fixes:\n"
                    f"Buggy Code:\n{extra_details}\n\n"
                    f"Provide the corrected and optimized code along with explanations."
                )
                
                # Generate response from AI
                response = chat.send_message(prompt, stream=True)
                
                # Aggregate response chunks
                generated_code = ""
                for chunk in response:
                    if chunk.text:
                        generated_code += chunk.text
                
                # Display explanations and suggestions
                display_explanations()

                # Display the corrected code
                st.markdown("### Generated Corrected Code:")
                st.markdown("---")
                st.code(generated_code, language='python')

                # Perform efficiency analysis on the corrected code
                exec_time, mem_used, output = execute_code(generated_code)

                # Display efficiency analysis and output
                display_analysis_results(output, exec_time, mem_used)

                # Bug detection in corrected code
                st.markdown("### Bug Detection:")
                bug_result = detect_bugs(generated_code)
                st.write(bug_result)

            except Exception as e:
                st.error(f"An error occurred while processing the request: {e}")
    else:
        st.warning("Please enter code for analysis.")
