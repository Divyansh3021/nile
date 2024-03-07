import os
import google.generativeai as genai

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
llm = genai.GenerativeModel('gemini-pro')

def get_folder_paths(directory = "githubCode"):
    folder_paths = []
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            # Skip the directory if a .git folder is found
            dirs.remove('.git') 
        for dir_name in dirs:
            folder_paths.append(os.path.join(root, dir_name))
    return folder_paths

directory_paths = get_folder_paths()

files = []

for directory_path in directory_paths:
    for filename in os.listdir(directory_path):
        if filename.endswith((".py",".js", ".ts")):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, "r", encoding='utf-8') as file:
                files.append(filepath)

def get_techstack():
    print(files)
    prompt= f"the files used in a project are these {files}. Based on this data, generate a file structure of this project."
    response = llm.generate_content(prompt)
    return response.text

techStack = get_techstack()