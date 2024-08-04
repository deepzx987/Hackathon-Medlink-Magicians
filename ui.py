#Import Streamlit
import streamlit as st
from PIL import Image
import streamlit as st
import seaborn as sns
#Other imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from time import sleep
#from dataloader import load_data, statistical_features
#from data_merge import filter_reformat, input_file_processing,corr_,filter_pannel,input_pannel
#import pandas_profiling
#from streamlit_pandas_profiling import st_profile_report
#from pandas_profiling import ProfileReport
#from plots import correlation_plots
#from conditional_group import conditional_group

st.set_page_config(page_title="BioInsights", layout="wide")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
                content:'Developed by Aditya and Deepankar'; 
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

st.title("Medlink Magicians")

Use_local_existing_files = 0

# if submit:

df_pr_day = st.sidebar.file_uploader('Prescribed Medicine Schedule')
# Prescribed Sensor Data File
df_de_day = st.sidebar.file_uploader('Patient Sensor Data')



tab1, tab2, tab3 = st.tabs(["Scheduler", "Probablistic Diagnosis", "Sensor Assisted Diagnosis"])


    
