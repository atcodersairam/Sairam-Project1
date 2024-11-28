import os
import re
import streamlit as st
import google.generativeai as genai
import time
import tracemalloc
from io import StringIO
import contextlib
import ast

# Hardcoded Google API Key
GOOGLE_API_KEY = "AIzaSyBm6NVne2mZpyc6abAACbKWnAcmlZ_FWbY"  # Replace this with your actual API key

# Configure Google Generative AI with the provided API key
genai.configure(api_key=GOOGLE_API_KEY)

# Use the "models/gemini-1.5-flash" model
model_name = "models/gemini-1.5-flash"
model = genai.GenerativeModel(model_name)
chat = model.start_chat(history=[])

# Streamlit UI
st.title("Enhanced Code Efficiency Analysis and Bug Detection")
st.write("Fix Bugs and Optimize Your Code.")

# Input for extra details using a longer text area for additional context or instructions
extra_details = st.text_area("Enter Code with Bugs", height=200)

# Function to execute code and capture execution time and memory usage
def execute_code(code):
    tracemalloc.start()
    start_time = time.time()
    
    f = StringIO()
    with contextlib.redirect_stdout(f):
        try:
            exec(code)  # Using exec to run user code
        except Exception as e:
            f.write(f"Error: {e}")
    
    end_time = time.time()
    memory_used = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    execution_time = end_time - start_time
    output = f.getvalue()
    
    return execution_time, memory_used, output

# Function to detect bugs in code
def detect_bugs(code):
    try:
        # Attempt to parse the code to detect syntax errors
        ast.parse(code)
        return "No syntax errors detected."
    except SyntaxError as e:
        return f"Syntax Error: {e}"
    except Exception as e:
        return f"Runtime Error: {e}"

# Submit button to get response
if st.button("Generate"):
    if extra_details:
        with st.spinner("Removing Bugs and Enhancing the Code..."):
            try:
                # Prompt for Google Generative AI
                prompt = (
                    f"Exection Time,Time Complexity,Bug Present"
                    f"Buggy Code:\n{extra_details}\n\n"
                    f"Fixed Code:\n which can be copied with clipboadrd button near the code "
                )

                # Sending the prompt to the Generative AI model
                response = chat.send_message(prompt, stream=True)

                output = ""
                for chunk in response:
                    if chunk.text:
                        output += chunk.text

                # Explanations Section (on top)
                st.markdown("### Explanation of Fixes and Enhancements:")
                st.markdown("---")
                st.markdown(""" 
                    **Algorithm Efficiency:**
                    The provided code had performance issues that resulted in higher-than-expected time complexity due to nested loops or inefficient data structures.
                    
                    **Time Complexity:**
                    After the changes, the algorithm achieves an `O(n)` or better complexity in most cases, ensuring better scalability with large datasets.

                    **Space Complexity:**
                    The new solution reduces the memory usage by optimizing data structures and avoiding unnecessary storage.

                    **Suggestions for Further Improvement:**
                    - Use Hash Tables or Sets to achieve better lookup times.
                    - Avoid nested loops and consider algorithms like Binary Search for searching large datasets.
                """)

                # Code Section (below explanations)
                st.markdown("### Generated Corrected Code:")
                st.markdown("---")
                st.code(output, language='python')  # Generated code in its own block

                # Perform efficiency analysis on the corrected code
                execution_time, memory_used, result_output = execute_code(output)

                # Show efficiency analysis results
                st.markdown("### Efficiency Analysis:")
                st.markdown(f"**Execution Time:** `{execution_time:.4f} seconds`")
                st.markdown(f"**Memory Used:** `{memory_used / 1024:.2f} KB`")

                # Show code output
                st.markdown("### Code Output:")
                st.code(result_output)

                # Bug detection on the corrected code
                st.markdown("### Bug Detection:")
                bug_detection_result = detect_bugs(output)
                st.write(bug_detection_result)

                # Efficiency discussion and alternatives
                st.markdown("### Efficiency Discussion and Alternatives:")
                st.markdown("""
                    The current solution works but may still be inefficient for larger datasets, depending on the specific algorithm used.
                    Alternative approaches include:
                    
                    - **Hash Table (Dictionary):** Reduces time complexity to `O(n)`.
                    - **Binary Search Tree (BST):** Allows for `O(log n)` search times, reducing the complexity for searching operations.
                """)

                # Additional Optimizations
                st.markdown("### Potential Further Optimizations:")
                st.markdown("""
                    - Consider multi-threading or parallel computing techniques for larger datasets.
                    - Avoid recalculating results; instead, store previously computed values to reduce redundant operations (Memoization).
                """)

            except Exception as e:
                st.error(f"An error occurred while processing the request: {e}")
    else:
        st.warning("Please enter code for analysis.")
