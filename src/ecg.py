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

def calculate_rr_intervals(peaks):
    rr_intervals = []
    for i in range(1, len(peaks)):
        rr_interval = peaks[i] - peaks[i-1]
        rr_intervals.append(rr_interval)
    return rr_intervals

def ECG_Rhythm_Prediction():
    filename = "100.csv"
    df = pd.read_csv(filename)
    plt.figure(figsize=(20,5))

    start = 0
    end = 1000
    interval = 120

    y = normalize(df['MLII'].values[:500000])
    chart = st.line_chart(y)

    filename='100annotations.txt'
    f = open(filename, 'rb')
    next(f)

    annotations = [line for line in f]
    peaks = [int(a.split()[1]) for a in annotations]
    rr_intervals = calculate_rr_intervals(peaks)
    rr_intervals = rr_intervals[1:]

    content_placeholder = st.empty()
    peak_interval = 1
    peak_start = 0
    peak_end = 1

    while True:
        chart.line_chart(y[start:end])
        for val in rr_intervals[peak_start:peak_end]:
            if val>285:
                content_placeholder.text("Patient is suffering from Tachycardia, Notification to Caregiver Sent")
            else:
                content_placeholder.text("Patient is Normal")

        start = start+interval
        end = end+interval

        peak_start = peak_start+peak_interval
        peak_end = peak_end+peak_interval
        time.sleep(1)

# ECG_Rhythm_Prediction()