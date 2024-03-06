import os
import streamlit as st
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

import git 

# embeddings = HuggingFaceHubEmbeddings(model="thuan9889/llama_embedding_model_v1")
from chromadb.utils import embedding_functions
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.environ['GOOGLE_API_KEY'], task_type="retrieval_query")

model = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=os.environ['GOOGLE_API_KEY'],temperature=0.2,convert_system_message_to_human=True)

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
directory_paths.append("Code")
print("directory_paths: ", directory_paths)

with open("Code.txt", "w", encoding='utf-8') as output:
    for directory_path in directory_paths:
        for filename in os.listdir(directory_path):
            if filename.endswith((".py",".ipynb",".js", ".ts")):
                filepath = os.path.join(directory_path, filename)
                with open(filepath, "r", encoding='utf-8') as file:
                    code = file.read()
                    output.write(f"Filepath: {filepath}:\n\n")
                    output.write(code + "\n\n")

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

loader = TextLoader("Code.txt", encoding="utf-8")
pages = loader.load_and_split()

# Split data into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
context = "\n\n".join(str(p.page_content) for p in pages)
texts = text_splitter.split_text(context)

vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k":5})

qa_chain = RetrievalQA.from_chain_type(
    model,
    retriever=vector_index,
    return_source_documents=True
)
    
# Function to generate assistant's response using ask function
def ask(question):
    answer = qa_chain({"query": question})
    print(answer)
    return answer['result']

# print(generate_assistant_response("Tell me about the instructor_embeddings function."))