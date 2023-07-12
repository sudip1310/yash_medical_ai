import streamlit as st
from pathlib import Path
import os, random
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
import openai
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from speech_to_text import * #edited by Sudip
import speech_recognition as sr
#from mic_access_streamlit import *
import tempfile
from st_custom_components import st_audiorec
from audio_recorder_streamlit import audio_recorder
from pydub import AudioSegment as am

r = sr.Recognizer()

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


# extract text from multiple pdf files
@st.cache_data()
def extract_text_multiple(pdfs_folder):
    # extracted_text = text = high_level.extract_text(pdf_path, "")
    raw_text = ""
    for pdf_file in pdfs_folder:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            temp_file.write(pdf_file.read())
           
        doc_reader = PdfReader(temp_path)
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


@st.cache_resource()
def get_chunk_lst(pdf_text):
    splitter = CharacterTextSplitter(
                separator = ".",
                chunk_size = 200,
                chunk_overlap = 100,
                length_function = len
            )
    chunk_lst = splitter.split_text(pdf_text)
    return chunk_lst

def member_page():
    #st.title("GenAI-Assisted Medical Records Extraction")
    st.markdown("<h1 style='text-align: center; color: black;'>Generative-AI Assisted Medical Records Extraction</h1>", unsafe_allow_html=True)
    # file selection dropdown menu
    # st.write("check out this [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
    # selected_file = st.selectbox("Select a PDF [[All Reports](https://drive.google.com/drive/folders/1BocjhYw5_XB6113__FNtL4eTt1mSpE3z)]",
    #                              pdf_files)
    pdfs_folder = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    
    
    #### OpenAI API Key
    #load_dotenv()
    # api = os.getenv("api_key")
    ##api = st.secrets["openai_api_key"]
    # os.environ["OPENAI_API_KEY"] = api

    # API key input field
    st.write("")
    st.write("")
    api_key = st.text_input("Enter Your API-key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

        st.write("")
        st.write("")
        st.write("")
        
        question=""
        # input question
        ask_text = st.text_input("Ask a Question")
        col1, col3,  col2 = st.columns([2, 3, 2])
        with col1:
            ask_button = st.button("Ask", use_container_width=1)
        with col2:
            # speak_button = st.button("Speak", use_container_width=1)
            # audio_bytes = audio_recorder(text="", icon_size="2x") -> small button
            audio_bytes = audio_recorder(text = "Click to record", icon_size="2x", key="audio_button")
            
        st.markdown(
            """
            <style>
                .body {
                    <button type="button" class="btn btn-primary">Primary</button>
                }
            </style>
            """,
                unsafe_allow_html=True,
        )
        
        # st.write("Click the 'Start' button and speak into your microphone.")
        if audio_bytes:
            text=""
            # question = text
            # audio_bytes = audio_recorder(text = "Click to record", icon_size="2x", key="audio_button")
            filename = str(random.randint(1,199))+".wav"
            with open(filename, mode='bx') as f:
                f.write(audio_bytes)
                sound = am.from_file(filename, format='wav', frame_rate=44100)
                sound = sound.set_frame_rate(16000)
                sound.export(filename, format='wav')
                harvard = sr.AudioFile(filename)
                with harvard as source:
                    audio = r.record(source)
                try:
                    text = r.recognize_google(audio)
                except Exception as e:
                    st.write("Try Again")
            
            os.remove(filename)
            # question_speech = speechTotext()  #edited by sudip
            question = text
            
        if ask_button:
            question = ask_text
        
        # output
        if question!="":
            st.write("You Asked:", question)
            st.write("please wait...")
            if pdfs_folder:
                # file_path = os.path.join(file_directory, selected_file)
                # pdf_text = extract_text(file_path)
                pdf_text = extract_text_multiple(pdfs_folder)
                ### GenerativeAI
                
        # Perform your time-consuming task or computation here
        
                chunk_lst = get_chunk_lst(pdf_text)
                embeddings = get_embeddings()
                doc_search = FAISS.from_texts(chunk_lst, embeddings)
                chain = get_qa_chain()
                query = question
                docs = doc_search.similarity_search(query)
                    #op = chain.run(input_documents=docs, question=query)
                try:
                    op = chain.run(input_documents=docs, question=query)
                    if (op==" I don't know." or op==" I'm sorry, I don't understand the question." or op=="I don't know." or op==" Sorry,i don't know"):
                        st.write("Apologies! The information you have requested is not available at this point")
                    else:
                        st.write(op)
                except Exception as e:
                    print("Error",e)
                    st.write("Apologies! The information you have requested is not available at this point")
            else:
                st.warning("Please select a PDF.")
            audio_bytes = False
            ask_button = False
            question=""
            
    # elif key_val_btn and api_key=="":
    #     st.error("Please, Enter Your API-Key")