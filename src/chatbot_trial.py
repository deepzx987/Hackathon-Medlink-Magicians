import streamlit as st
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
import csv
import pyttsx3
import re
import random
from streamlit_chat import message
from sklearn import tree as _tree

def Assistive_Diagnosis_trial():
    st.header("Welcome to the Assistive Diagnosis Chatbot")
    st.write("This chatbot will help you to diagnose your disease based on your symptoms")
    # initialise the container for the data
    # Layout of input/response containers
    ## generated stores AI generated responses
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["How can the Medlink Magicians help you today?"]
    ## past stores User's questions
    if 'past' not in st.session_state:
        st.session_state['past'] = ['Hi!']

    if "history" not in st.session_state:
        st.session_state.history = []

    response_container = st.container()
    input_container = st.container()

    def clear_chat() -> None:
        st.session_state.generated = []
        st.session_state.past = []
        st.session_state.history = []

    st.button(label="clear chat history", on_click=clear_chat)
    

    def generate_response(prompt):
        greetings = ["hi", "hello", "hey", "greetings", "sup", "what's up", "hey there"]
        greetings_response = ["How can the Medlink Magicians help you today? Please help me with your name."]
        symptoms_prompt = "Enter the symptom you are experiencing"
        
        if prompt in greetings:
            response = random.choice(greetings_response)
            return response
        
        elif re.search(r"not feeling well", prompt, re.IGNORECASE):
            response = symptoms_prompt
            return response
        
        elif re.search(r"Deepankar", prompt, re.IGNORECASE):
            response = "Hi Deepankar! " + symptoms_prompt + "\n * Nausea \n * Headache \n * Backpain \n * Fever"
            return response
        
        elif re.search(r"Nausea", prompt, re.IGNORECASE):
            response = "Have you experienced this type of nausea before? (Yes/No)"
            return response
        
        elif re.search(r"Yes", prompt, re.IGNORECASE):
            response = "Are you currently taking any medications? Like these below: \n * Ondansetron (Zofer, Emeset) \n * Domperidone (Domstal, Motilium) \n * Metoclopramide (Perinorm, Reglan) \n * Doxylamine (Vomikind)"
            return response
        
        elif re.search(r"Ondansetron", prompt, re.IGNORECASE):
            response = "Do you have headaches? (No/Yes)"
            return response
        
        elif re.search(r'No', prompt, re.IGNORECASE):
            response = "Are you at home or outside?"
            return response

        elif re.search(r'At home', prompt,re.IGNORECASE):
            response = 'Here are some suggestions to help you: \n * Ginger: Ginger has been used for centuries as a natural remedy for nausea. You can try consuming ginger in various forms, such as ginger tea, ginger ale, ginger candies, or chewing on a piece of fresh ginger. \
                        \n * Peppermint: Peppermint is another natural remedy that may help soothe an upset stomach and relieve nausea. You can try sipping on peppermint tea or sucking on peppermint candies. \
                        \n * Communicate with your healthcare provider: Keep your healthcare provider informed about your experience with Ondansetron'
            return response
        
        else:
            response = "What is your name?"
            return response

    def get_text():
        input_text = st.text_input("You: ", "", key="input")
        return input_text
    
    with input_container:
        user_input = get_text()
    
    with response_container:
        if user_input:
            response = generate_response(user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)
            
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))


