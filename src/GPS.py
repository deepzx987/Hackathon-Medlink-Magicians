import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd

def normalize(data):
    min_val = np.min(data)
    max_val = np.max(data)
    normalized_data = (data - min_val) / (max_val - min_val)
    return normalized_data

def geolocation_analysis():
    x=3
    y=x
    filename = "halt.csv"
    data = pd.read_csv(filename, parse_dates=['Timestamp'])
    # plt.figure(figsize=(x,y))

    # if ax is None:
    #     plt.figure(figsize=(5, 5))
    # else:
    #     plt.sca(ax)

    # Prepare Streamlit components
    chart_placeholder = st.empty()
    notification_placeholder = st.empty()

    start = 0
    end = 1
    same_location_counter = 1
    same_location_duration = pd.Timedelta(seconds=0)
    previous_location = None

    while end < len(data):
        plt.figure(figsize=(x,y))
        # Update scatter chart
        locations = data['Location'].iloc[start:end].str.extract(r'\(([-+]?\d+\.\d+), ([-+]?\d+\.\d+)\)')
        locations = locations.astype(float)
        plt.scatter(locations[1], locations[0])
#         normalized_locations = normalize(locations)
#         plt.scatter(normalized_locations[1], normalized_locations[0])
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        # plt.title('Geolocation Analysis')
         # Normalize latitude and longitude
        normalized_locations = normalize(locations)

        # Plot scatter chart using Streamlit
        plt.xlim(-77,-73)
        plt.ylim(39,51)
        plt.scatter(normalized_locations[1], normalized_locations[0])
        chart_placeholder.pyplot(plt.gcf(), use_container_width=False)


        # Check if the person has been in the same location for more than 5 seconds
        if same_location_counter > 4 :#and same_location_duration > pd.Timedelta(seconds=4):
            notification_placeholder.text("Person has been in the same location for more than 5 seconds")
            #print('yes')
        else:
            notification_placeholder.text("Person has not been in the same location for more than 5 seconds")
            #print('no')

        # Update indices for the next iteration
        start += 1
        end += 1

        # Check if the location remains the same
        current_location = (locations[0].iloc[-1], locations[1].iloc[-1])
        if previous_location is not None and current_location == previous_location:
            same_location_counter += 1
            same_location_duration += data['Timestamp'].iloc[end - 1] - data['Timestamp'].iloc[end - 2]
        else:
            same_location_counter = 1
            same_location_duration = pd.Timedelta(seconds=0)
        #print(locations,previous_location,same_location_counter,same_location_duration)

        # Store the current location as the previous location for the next iteration
        previous_location = current_location

        # Delay for visualization
        time.sleep(1)
#         plt.show()
        plt.clf()
    # return plt

# Run the geolocation analysis using Streamlit
# geolocation_analysis()
