#Import Streamlit
import streamlit as st
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime, os
from reminders import *
from messaging import *

st.set_page_config(page_title="Medlink Magicians", layout="wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
                content:'Developed by Souptik, Deepti, Asit, Rashmie and Deepankar'; 
                visibility: visible;
                display: block;
                position: relative;
                #background-color: red;
                padding: 10px;
                top: 5px;
                left: 600px;
            }
            div.abs{
                # display: flex;
                # flex-direction: column;
                # justify-content: space-between;
                # display:block
                # position: fixed;
                #position: -webkit-sticky; /* safary */
                #position: sticky;
                # bottom: 0px;
                top: 100px;
                left: 1000px;
                padding: 10px;
                #width: 100%;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def write_heading_in_tab(title,font_size):
    st.markdown("<h1 style='text-align: center; font-style: italic; font-size: {}px;'>{}</h1>".format(font_size, title), unsafe_allow_html=True)

st.title("We Are Medlink Magicians!")
# st.sidebar.image('Image/img2.jpeg')

# # Patient Reported Outcome File
# df_pr_day = st.sidebar.file_uploader('Patient Reported Outcome File')
# # Physical Endpoint Features File
# df_de_day = st.sidebar.file_uploader('Physical Endpoint Features File')

tab1, tab2, tab3 = st.tabs(["Reminder", "Assistive Diagnosis", "Sensor Based Prediction"])

with tab1:
    schedule_id = str(1)
    patient_id = str(1)
    date_time = datetime.datetime.now()

    # Add a title to your app
    st.title("If Doctor Wants to Enter Details")


    # Create two columns for input
    col1, col2, col3 = st.columns(3)

    # Get user input in the first column
    with col1:
        medicine_name = st.text_input("Enter Medicine Name")

    # Get user input in the second column
    with col2:
        symptom = st.text_input("Enter symptom")

    # Get user input in the second column
    with col3:

        # Add a title to your app
        # st.title("Enter instructions")
        # Define options for the dropdown menu
        options = ["Before food", "After food"]
        instructions = st.selectbox("Enter instructions", options)

    # # Display the inputs
    st.write("schedule_id:", schedule_id)
    st.write("patient_id:", patient_id)
    st.write("Date:", str(date_time.date()))
    st.write("Time:", str(date_time.time()))
    st.write("medicine_name:", medicine_name)
    st.write("symptom:", symptom)
    st.write("instructions:", instructions)

    # medicine_name='Paracetamol'
    # symptoms='Headache'
    # # instructions=After food

    # Set Required Paths and Control Parameters
    project_root_dir = os.path.dirname(os.getcwd())
    data_dir = os.path.join(project_root_dir,'data')
    reminder_threshold_past_mins = 30
    reminder_threshold_future_mins = 10

    medicine_schedule_file_path = os.path.join(data_dir,'medicine_schedule.csv')
    patient_info_file_path = os.path.join(data_dir,'patient_info.csv')

    medicine_schedule_file_path = pd.read_csv(medicine_schedule_file_path) # type: ignore
    patient_info_file_path = pd.read_csv(patient_info_file_path) # type: ignore

    
    st.write('medicine_schedule_file_path')
    st.dataframe(medicine_schedule_file_path.head()) # type: ignore

    st.write('patient_info_file_path')
    st.dataframe(patient_info_file_path.head()) # type: ignore
    

    lst_reminder_messages = fetch_medicine_reminders(medicine_schedule_file_path, patient_info_file_path)

    print (lst_reminder_messages[0])
    # print (lst_reminder_messages[1])
    # print (lst_reminder_messages[2])

    # st.write(lst_reminder_messages)


    options = ["Yes", "No"]
    medicine_taken = st.selectbox("medicine_taken?", options)
    # medicine_taken = st.text_input("medicine_taken?")

    if medicine_taken=='Yes':

        number = lst_reminder_messages[0][1]
        msg_content = lst_reminder_messages[0][2]
        print (msg_content)
        print (number)
        # send_message(msg_content, number)
        options = ["Yes", "No"]
        taken_on_time = st.selectbox("Did you follow instruction?", options)
        response=1

        if taken_on_time=="No":
            st.write('Please take your medicine on time.')
            response=None

    else:
        st.write('Please take your medicine.')
        taken_on_time="No"
        response=None

    lst_reminder_response = [(schedule_id, medicine_taken, taken_on_time)]
    update_medicine_reminders(medicine_schedule_file_path, lst_reminder_response)

    with tab2:
        st.write('Chatbot based Assistive Diagnosis')
        
    with tab3:
        st.write('Sensor Based Prediction')