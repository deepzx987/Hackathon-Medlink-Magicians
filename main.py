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
from dataloader import load_data, statistical_features
from data_merge import filter_reformat, input_file_processing,corr_,filter_pannel,input_pannel
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
from pandas_profiling import ProfileReport
from plots import correlation_plots
from conditional_group import conditional_group

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

st.title("Welcome to BioInsights!")
st.sidebar.image('Image/img2.jpeg')

# Use_local_existing_files = [True, False]
# Use_local_existing_files = st.selectbox("Use Local Existing Files:", Use_local_existing_files)
# submit = st.button("Submit", key=1)
Use_local_existing_files = 0

# if submit:
if Use_local_existing_files:
    df_pr_day = pd.read_csv('../Data/adnrs_bp02_.csv')
    df_de_day = pd.read_csv('../Data/bp02_physiq_PA_endpoints_daily.csv')

else:
    # Patient Reported Outcome File
    df_pr_day = st.sidebar.file_uploader('Patient Reported Outcome File')
    # Physical Endpoint Features File
    df_de_day = st.sidebar.file_uploader('Physical Endpoint Features File')

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["Data Display", "Data Statistics", "Find Correlation","Conditional Data Grouping and Analysis","Feature Extraction", "Exploratory Data Analysis", "Feature Reduction/Selection", "Modelling", "Testing"])

if df_pr_day is not None and df_de_day is not None:

    if Use_local_existing_files:
        pass
    else:
        df_pr_day = pd.read_csv(df_pr_day) # type: ignore
        df_de_day = pd.read_csv(df_de_day) # type: ignore

    df_pr_day.columns = df_pr_day.columns.str.lower() # type: ignore
    df_de_day.columns = df_de_day.columns.str.lower() # type: ignore
    
    with tab1:
        
        st.write('Patient Reported Outcome')
        st.dataframe(df_pr_day.head()) # type: ignore

        st.write('Physical Endpoint Features')
        st.dataframe(df_de_day.head()) # type: ignore
        
    # with tab2:
        
    #     st.title("Data Statistics")
    #     profile = ProfileReport(df_de_day, # type: ignore
    #                             minimal = False, # type: ignore
    #                             explorative = False, 
    #                             sensitive = False, 
    #                             dark_mode = False, 
    #                             orange_mode = False, 
    #                             tsmode = False, 
    #                             sortby = None, 
    #                             sample = None, 
    #                             config_file = None, # type: ignore
    #                             lazy = True) # type: ignore
    #     st_profile_report(profile)
    #     profile.to_file("../Data/output.html")
    #     profile.to_file("../Data/output.json")
    
    
    with tab3:

        # d_de_select_day = {'granularity_col':'local_date', 
        #                 'date_format':'%Y-%m-%d' , 
        #                 'subject_col':'subject',
        #                 'data_format':'wide_format',
        #                 'dimensions':['Steps Count', 'Average Step-to-Step Interval', 'Bouts Count', 'Longest Period of Walking', 
        #                                 'Steps / Bout', 'Gait Rate', 'Standard Deviation Gait Rate', 'Cadence',
        #                                 '90th Percentile Step-to-Step Interval', 'Step Rate Change', '30 MAM',
        #                                 'Moderate to Vigorous Physical Activity'],
        #                 'filter': {'is_compliant':[True]}}
        # d_de_select_day['dimensions'] = list(pd.Series(d_de_select_day['dimensions']).str.lower())

        # d_pr_select_day = {'granularity_col':'aendt', 
        #                 'date_format':'%d%b%Y', 
        #                 'subject_col':'subjid',
        #                 'data_format':'long_format',
        #                 'dimensions':['PARAMCD'],
        #                 'dimension_value':'aval',
        #                 'filter':{}}
        # d_pr_select_day['dimensions'] = list(pd.Series(d_pr_select_day['dimensions']).str.lower())

        # d_de_select_day = {}
        # d_pr_select_day = {}

    
        granularity = ["day","visit", "biweekly", "weekly"]
        granularity = st.selectbox("Granularity:", granularity)


        # filter pannel to subset patient and digital end point report
        pr_selected_values,de_selected_values = filter_pannel(df_pr_day,df_de_day)

        # input pannel to take user input
        selected_values_dict = input_pannel(df_pr_day,df_de_day)

        #updating input pannel dictionary, adding filter key
        selected_values_dict['pr_select']['filter'] = pr_selected_values
        selected_values_dict['de_select']['filter'] = de_selected_values

        if(granularity=='day'):
            # keeping date format constant
            selected_values_dict['pr_select']['date_format'] = '%d%b%Y'
            selected_values_dict['de_select']['date_format'] = '%Y-%m-%d'

        #extracting input JSON
        d_de_select_day = selected_values_dict['de_select']
        d_pr_select_day = selected_values_dict['pr_select']

        if st.button("Submit"):
            st.session_state['submitted'] = True

        if 'submitted' not in st.session_state:
                st.session_state['submitted'] = None
            
        if st.session_state['submitted']:
            df_merge = input_file_processing(df_pr_day, df_de_day, d_pr_select_day, d_de_select_day, granularity) # type: ignore
            st.write("Merged Dataframe")
            st.dataframe(df_merge)

            # function to find out correlation values
            df_corr_pearson_,de_dimension,pr_dimension = corr_(df_merge,df_pr_day, df_de_day,d_pr_select_day,d_de_select_day,'pearson')
            df_corr_spearman_,de_dimension,pr_dimension =  corr_(df_merge,df_pr_day, df_de_day,d_pr_select_day,d_de_select_day,'spearman')


            # function to do plots for inter and intra correlation
            correlation_plots(df_merge,df_corr_pearson_,df_corr_spearman_,de_dimension,pr_dimension)

            with tab4:

                # str.write("inprogress")
                conditional_group(df_merge)
    
    # with tab4:




    #     with tab3:

    #         st.title("This is Feature Extraction")
    #         st.write("File Uploaded --> Change Later to Create Upload File Option")
    #         Data, unique_days  = load_data()
    #         st.write("Preview of the uploaded dataset:")
    #         st.dataframe(Data.head())
            
    #         for days in unique_days:
    #             specific_date_data = Data.loc[days]
    #             specific_date_data = specific_date_data.reset_index()
    #             specific_date_data = specific_date_data.dropna()
    #             signal_data = np.array(np.linalg.norm(specific_date_data[['acc_x', 'acc_y', 'acc_z']], axis=1))            
    #             mean, median, std, variance, min_value, max_value, range_value, quantile_25, quantile_75, rms, zero_crossing_rate, skewness, kurtosis, crest_factor, peak_to_average_ratio = statistical_features(signal_data)

    #         st.write("Mean:", mean)
    #         st.write("Median:", median)
    #         st.write("Standard Deviation:", std)
    #         st.write("Variance:", variance)
    #         st.write("Minimum Value:", min_value)
    #         st.write("Maximum Value:", max_value)
    #         st.write("Range:", range_value)
    #         st.write("25th Percentile (Q1):", quantile_25)
    #         st.write("75th Percentile (Q3):", quantile_75)
    #         st.write("Root Mean Square (RMS):", rms)
    #         st.write("Zero Crossing Rate:", zero_crossing_rate)
    #         st.write("Skewness:", skewness)
    #         st.write("Kurtosis:", kurtosis)
    #         st.write("Crest Factor:", crest_factor)
    #         st.write("Peak-to-Average Ratio:", peak_to_average_ratio)
            
        # with tab4:
            
        #     st.title("This is Exploratory Data Analysis")
            
        # with tab5:
            
        #     st.title("This is Feature Reduction and Selection")
                
        # with tab6:
            
        #     st.title("This is Modelling")
                    
        # with tab7:
            
        #     st.title("This is Testing")