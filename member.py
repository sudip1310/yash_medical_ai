import streamlit as st
from pathlib import Path
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
import openai
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS 
from speech_to_text import * #edited by Sudip


# extract text from pdf
@st.cache_data()
def extract_text(pdf_path):
    # extracted_text = text = high_level.extract_text(pdf_path, "")
    doc_reader = PdfReader(pdf_path)
    raw_text = ""
    for page in doc_reader.pages:
        raw_text += page.extract_text()
    # raw_text = raw_text.replace(' ', '')
    # raw_text = raw_text.replace('\n', ' ')
    return raw_text

# get a response
def get_answer(query, pdf_text):
    answer = f'query:\n{query}\n\nextracted text:\n{pdf_text}'
    return answer

# get the list of pdf files
file_directory = os.path.join(Path.cwd(),"file_directory")
# pdf_files = [f'sample{i}.pdf' for i in range(1, len(os.listdir(file_directory))+1)]
pdf_files = sorted([file for file in os.listdir(file_directory)])

@st.cache_resource()
def get_embeddings():
    return HuggingFaceEmbeddings()

@st.cache_resource()
def get_qa_chain():
    return load_qa_chain(OpenAI(), chain_type="stuff")

def member_page():
    st.title("AI Assisted Medical Records Digitization")
    
    # file selection dropdown menu
    # st.write("check out this [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
    selected_file = st.selectbox("Select a PDF [[All Reports](https://drive.google.com/drive/folders/1BocjhYw5_XB6113__FNtL4eTt1mSpE3z)]",
                                 pdf_files)

    ### OpenAI API Key
    # load_dotenv()
    # api = os.getenv("openai_api_key")
    api = st.secrets["openai_api_key"]
    os.environ["OPENAI_API_KEY"] = api

    question=""
    # input question
    question = st.text_input("Ask a Question")
    
    col1, col2 = st.columns([1,1])
    with col1:
        ask_button = st.button("Ask", use_container_width=1)
    with col2:
        speak_button = st.button("Speak", use_container_width=1)
    
    # st.write("Click the 'Start' button and speak into your microphone.")
    if speak_button:
        question_speech = speechTotext()  #edited by sudip
        question = question_speech



    # output
    if question!="":
        if selected_file:
            file_path = os.path.join(file_directory, selected_file)
            pdf_text = extract_text(file_path)

            ### GenerativeAI
            splitter = CharacterTextSplitter(
            separator = ".",
            chunk_size = 200,
            chunk_overlap = 100,
            length_function = len
            )
            chunk_lst = splitter.split_text(pdf_text)

            embeddings = get_embeddings() 
            doc_search = FAISS.from_texts(chunk_lst, embeddings)

            chain = get_qa_chain()
            
            query = question
            docs = doc_search.similarity_search(query)
            op = chain.run(input_documents=docs, question=query)
            
            st.write(op)
        else:
            st.warning("Please select a PDF.")
