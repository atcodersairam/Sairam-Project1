import streamlit as st
import requests
import re
import math  # For IDF calculation

# GitHub Token (Hardcoded)
GITHUB_TOKEN = "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"

def fetch_file_content(file_url, headers=None):
    """Fetches the content of a file from GitHub(URL)."""
    try:
        file_response = requests.get(file_url, headers=headers)
        file_response.raise_for_status()
        return file_response.text
    except requests.exceptions.RequestException as e:
        return f"Could not fetch file content: {e}"

def find_file_url(repo_url, filename):
    """
    Finds the download URL of a specified file within a GitHub repository.
    If the file is found, returns the file's download URL; otherwise, returns None.
    """
    if "github.com" in repo_url:
        parts = repo_url.rstrip('/').split('/')
        if len(parts) < 5:
            return "Invalid repository URL format. Example: https://github.com/user/repository"
        
        owner, repo = parts[3], parts[4]
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else None

        def search_for_file(api_url, filename):
            try:
                response = requests.get(api_url, headers=headers)
                response.raise_for_status()
                contents = response.json()
                for item in contents:
                    if item['type'] == 'file' and item['name'] == filename:
                        return item['download_url']
                    elif item['type'] == 'dir':
                        found_url = search_for_file(item['url'], filename)
                        if found_url:
                            return found_url
            except requests.exceptions.RequestException as e:
                return f"Could not search for file: {e}"
            return None

        return search_for_file(api_url, filename)
    else:
        return "Invalid GitHub URL."

def search_related_files(query, token=GITHUB_TOKEN, per_page=10, page=1):
    """
    Searches for files on GitHub related to a specific query.
    """
    base_url = "https://api.github.com/search/code"
    headers = {"Authorization": f"token {token}"} if token else None

    # Refine the query to search for files globally
    refined_query = f"{query} in:file"
    params = {"q": refined_query, "per_page": per_page, "page": page}

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return [{"name": item['name'], "url": item['html_url'], "download_url": item['repository']['url'] + "/contents/" + item['path']} for item in data.get('items', [])], response.links.get('next') is not None
    except requests.exceptions.RequestException as e:
        return f"Error searching related files: {e}", False

def calculate_term_frequency(content, term):
    """Calculates the term frequency (TF) of a term in the given content."""
    term = term.lower()
    words = content.lower().split()
    term_count = words.count(term)
    total_words = len(words)
    return term_count / total_words if total_words > 0 else 0

def calculate_inverse_document_frequency(files, term):
    """Calculates the inverse document frequency (IDF) of a term across all files."""
    term = term.lower()
    doc_count = 0
    for file in files:
        file_content = fetch_file_content(file['download_url'], headers={"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else None)
        if file_content and term in file_content.lower():
            doc_count += 1
    return math.log(len(files) / (1 + doc_count)) if doc_count > 0 else 0

def rank_files_by_tfidf(files, term):
    """Ranks files based on the TF-IDF score of the term in their content."""
    ranked_files = []
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else None

    # Calculate IDF for the term
    idf_score = calculate_inverse_document_frequency(files, term)
    
    for file in files:
        file_content = fetch_file_content(file['download_url'], headers)
        if file_content:
            tf_score = calculate_term_frequency(file_content, term)
            tfidf_score = tf_score * idf_score
            ranked_files.append({"name": file['name'], "url": file['url'], "tfidf_score": tfidf_score})

    # Sort files by TF-IDF score in descending order
    ranked_files.sort(key=lambda x: x['tfidf_score'], reverse=True)
    return ranked_files

def extract_function_names(content):
    """Extracts function names from the given content using regular expressions."""
    return re.findall(r"def\s+(\w+)\s?\(", content)

def main():
    # Streamlit UI
    st.title("External-Knowledge")

    st.subheader("Choose")
    with st.form(key='main_form'):
        repo_url = st.text_input("GitHub repository URL:", "")
        filename = st.text_input("Filename:", "")
        fetch_file_action = st.form_submit_button("Fetch File Content")

        search_term = st.text_input("Enter a search term to find related files:", "")
        rank_files_action = st.form_submit_button("Search and Rank Related Files")
    
    if fetch_file_action:
        if repo_url and filename:
            file_url = find_file_url(repo_url, filename)
            if file_url:
                file_content = fetch_file_content(file_url, headers={"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else None)
                if file_content:
                    st.subheader(f"Content of '{filename}':")
                    st.text(file_content)
                    line_count = file_content.count('\n') + 1
                    st.write(f"Total number of lines: {line_count}")
                    
                    functions = extract_function_names(file_content)
                    if functions:
                        st.subheader("Functions:")
                        st.write(", ".join(functions))
                else:
                    st.error("Could not fetch the file content.")
            else:
                st.error(f"The file '{filename}' was not found.")
        else:
            st.warning("Enter both repository URL and filename.")
    
    if rank_files_action:
        if search_term:
            st.info(f"Searching for files related to '{search_term}'...")
            related_files, has_next_page = search_related_files(search_term)
            if related_files and not isinstance(related_files, str):
                ranked_files = rank_files_by_tfidf(related_files, search_term)
                if ranked_files:
                    st.subheader("Ranked Related Files:")
                    for file in ranked_files:
                        st.write(f"[{file['name']}]({file['url']})")
                else:
                    st.warning("No files found to rank.")
            else:
                st.error(related_files or "Error occurred.")
        else:
            st.warning("Enter a search term.")

if __name__ == "__main__":
    main()   
