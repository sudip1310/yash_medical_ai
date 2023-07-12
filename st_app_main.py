# streamlit_audio_recorder by stefanrmmr (rs. analytics) - version January 2023

import streamlit as st
from st_custom_components import st_audiorec
import os
import speech_recognition as sr

# Assuming you have the `wav_audio_data` variable containing the audio data
folder_path = 'audio_files'  # Replace with the actual folder path

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def audiorec_demo_app():

    # TITLE and Creator information
    st.title('streamlit audio recorder')
    # TUTORIAL: How to use STREAMLIT AUDIO RECORDER?
    # by calling this function an instance of the audio recorder is created
    # once a recording is completed, audio data will be saved to wav_audio_data

    wav_audio_data = st_audiorec() # tadaaaa! yes, that's it! :D

    # add some spacing and informative messages
    col_info, col_space = st.columns([0.57, 0.43])
    if wav_audio_data is not None:
        # display audio data as received on the Python side
        col_playback, col_space = st.columns([0.58,0.42])
        with col_playback:

            st.audio(wav_audio_data, format='audio/wav')
            file_path = os.path.join(folder_path, '1.wav')
            with open(file_path, 'wb') as file:
                file.write(wav_audio_data)

            print(f"Audio file saved at: {file_path}")

    recognizer = sr.Recognizer()

        # Load the audio file
    with sr.AudioFile("audio_files/1.wav") as source:
        text=""
        audio = recognizer.record(source)  # Read the entire audio file
        # Use the recognizer to convert audio to text
        text = recognizer.recognize_google(audio)
        st.write("You said:", text)
        print(text)

 # Replace with the actual file path

# Check if the file exists before attempting to delete it
       




if __name__ == '__main__':
    # call main function
    audiorec_demo_app()