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
from panel1 import *
# from chat_bot import *
from chatbot_trial import *
# from fall_detection import *
from ecg import *
from GPS import *

st.set_page_config(page_title="Medlink Magicians", layout="wide")
st.markdown("""
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
        .title {
            text-align: center;
            color: white;
            background-color: #da544a;
            padding: 10px;
            border-radius: 10px;
        }
        .header{
            text-align: center;
            font-family: Times New Roman;
        }
        .subheader{
            text-align: center;
            font-family: Times New Roman;
        }
        body {
            background-color: red;
            background-size: cover;
            background-image: "med_img";
            color: white;
        }
        .expander-content p {
            font-weight: bold;
        }
        .expander-content b {
            font-weight: bold;
        }
        .expander-header {
            font-weight: bold;
            font-size: 20px;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown('<h1 class="title">Medlink Magicians</h1>', unsafe_allow_html=True)
st.sidebar.image('medimg.png')

def main():

    # Define sidebar options
    panel_options = ["Reminder", "Assistive Diagnosis", "Sensor Based Prediction"]

    # Display the sidebar
    selected_panel = st.sidebar.selectbox("Select a panel", panel_options)

    # Display content based on the selected panel
    if selected_panel == "Reminder":
        Reminder()
    elif selected_panel == "Assistive Diagnosis":
        st.title("Patient's Personal Medical Assistant")
        Assistive_Diagnosis_trial()
    elif selected_panel == "Sensor Based Prediction":
        st.title("Digital Biomarker Monitoring")
        show_panel3()

def show_panel3():
    # content_placeholder = st.empty()
    tab1, tab2, tab3 = st.tabs(["None", "ECG Rhythm Prediction", "Patient Tracking"])
    
    with tab1:
        plt.clf()
        # content_placeholder.text("Please Select a functionality:")    

    with tab2:
        plt.clf()
        st.header("Heart Rate Based ECG Rhythm Prediction")
        ECG_Rhythm_Prediction()
        plt.clf()
    
    with tab3:
        plt.clf()
        st.header("GPS Based Patient Tracking")
        # geolocation_analysis()
        plt.clf()

    # with tab4:
    #     plt.clf()
    #     st.header("Accelerometer Based Fall Detection")
    #     # SBD()
    #     plt.clf()
    
if __name__ == '__main__':
    main()
