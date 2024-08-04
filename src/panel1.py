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
# import time

def Reminder():
    st.title("Reminder (Doctor's Upload Prescription Schedule)")
    options = ["No", "Yes"]
    doctor_detail = st.selectbox("Doctor, Do You Want to Enter Details?", options)
    # medicine_taken = st.text_input("medicine_taken?")

    if doctor_detail=='Yes':
        date_time = datetime.datetime.now()
        date = date_time.date()
        time = str(date_time.hour)+':'+str(date_time.minute)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            schedule_id = str(st.text_input("Schedule ID"))
        with col2:
            patient_id = str(st.text_input("Patient ID"))
        with col3:
            medicine_name = st.text_input("Medicine Name")
        with col4:
            symptom = st.text_input("Symptoms")
        with col5:
            options = ["Before food", "After food"]
            instructions = st.selectbox("Enter Instructions", options)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.write("Schedule ID:", schedule_id)
            st.write("Patient ID:", patient_id)
        with col2:
            st.write("Date:", str(date))
            st.write("Time:", str(time))
        with col3:
            st.write("Medicine:", medicine_name)
        with col4:
            st.write("Symptoms:", symptom)
        with col5:
            st.write("Instructions:", instructions)

    else:
        project_root_dir = os.path.dirname(os.getcwd())
        data_dir = os.path.join(project_root_dir,'data')
        medicine_schedule_file_path = os.path.join(data_dir,'medicine_schedule.csv')
        patient_info_file_path = os.path.join(data_dir,'patient_info.csv')
        medicine_schedule_file_path = pd.read_csv(medicine_schedule_file_path) # type: ignore
        patient_info_file_path = pd.read_csv(patient_info_file_path) # type: ignore

        
        # st.write('Upload Medicine Schedule File')
        uploaded_file = st.file_uploader("Upload Medicine Schedule File")
        if uploaded_file is not None:
            medicine_schedule_file_path = pd.read_csv(uploaded_file)
            st.dataframe(medicine_schedule_file_path.head()) # type: ignore

        # st.write('Upload Patient Information File')
        uploaded_file1 = st.file_uploader("Upload Patient Information File")
        if uploaded_file1 is not None:
            patient_info_file_path = pd.read_csv(uploaded_file1)
            st.dataframe(patient_info_file_path.head()) # type: ignore
        
        if uploaded_file1 is None or uploaded_file is None:
            return 

        st.write('Sending Reminder for Taking Medication')
        lst_reminder_messages = fetch_medicine_reminders(medicine_schedule_file_path, patient_info_file_path)
        st.write('\n')
        
        number = lst_reminder_messages[0][1]
        msg_content = lst_reminder_messages[0][2]
        send_message(msg_content, number)
        st.write('Reminder Sent')
        
        st.title("Requesting Patient Acknowledgement")

        options = ["No", "Yes"]
        medicine_taken = st.selectbox("Have You Taken The Medicine?", options)
        if medicine_taken=='Yes':
            st.write('Thanks.')
            options = ["No", "Yes"]
            taken_on_time = st.selectbox("Did you Take The Medicine on Time?", options)
            st.write('Thanks.')
            # response=1
            if taken_on_time=="No":
                st.write('Please take your medicine on time.')
                # response=None
        else:
            st.write('Please take your medicine.')
            taken_on_time="No"
            # response=None
        # lst_reminder_response = [(schedule_id, medicine_taken, taken_on_time)]
        # update_medicine_reminders(medicine_schedule_file_path, lst_reminder_response)
