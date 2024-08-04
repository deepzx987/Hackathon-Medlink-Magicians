import pandas as pd
import datetime
import os
import streamlit as st

# Set Required Paths and Control Parameters
project_root_dir = os.path.dirname(os.getcwd())
data_dir = os.path.join(project_root_dir,'data')
reminder_threshold_past_mins = 30
reminder_threshold_future_mins = 10

medicine_schedule_file_path_temp = os.path.join(data_dir,'medicine_schedule.csv')
patient_info_file_path_temp = os.path.join(data_dir,'patient_info.csv')

def get_date_description(date):
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(days=1)
    yesterday = today + datetime.timedelta(days=-1)

    if date.date() == today:
        return "Today"
    elif date.date() == tomorrow:
        return "Tomorrow"
    elif date.date() == yesterday:
        return "Yesterday"
    else:
        return date.strftime('%A')

def fetch_medicine_reminders(medicine_schedule_file_path, patient_info_file_path):

    # Read the Patient and Medicine Schedule Info and store it in respective dataframe
    # medicine_schedule_df = pd.read_csv(medicine_schedule_file_path)
    # patient_info_df = pd.read_csv(patient_info_file_path)
    
    medicine_schedule_df = medicine_schedule_file_path.copy()
    patient_info_df = patient_info_file_path.copy()
    medicine_schedule_df["datetime"] = pd.to_datetime(medicine_schedule_df['date'] + ' ' + medicine_schedule_df['time'])
    medicine_schedule_df['medicine_response'] = medicine_schedule_df['medicine_response'].astype(str)
    medicine_schedule_df['medicine_response'] = medicine_schedule_df['medicine_response'].str.title()

    # Filter the reminders to be sent today
    current_time = datetime.datetime.now()
    start_time = current_time - datetime.timedelta(minutes=reminder_threshold_past_mins)
    end_time = current_time + datetime.timedelta(minutes=reminder_threshold_future_mins)

    curr_reminder_df = medicine_schedule_df[(medicine_schedule_df['datetime'] >= start_time) & (medicine_schedule_df['datetime'] <= end_time)]

    not_responded_curr_reminder_df = curr_reminder_df[curr_reminder_df['medicine_response'] !='Yes']
    not_responded_curr_reminder_df.reset_index(inplace=True, drop=True)

    lst_reminder_messages = []
    for index, row in not_responded_curr_reminder_df.iterrows():
        schedule_id = row['schedule_id']
        patient_id = row['patient_id']
        curr_patient_info_df = patient_info_df[patient_info_df['patient_id']==patient_id]
        patient_name = curr_patient_info_df['patient_name'].values[0]
        mobile_number = curr_patient_info_df['mobile_number'].values[0]
        medicine_name = row['medicine_name']
        dosage_time = row['time']
        dosage_datetime = row['datetime']
        dosage_instructions = row['instructions']
        dosage_time_obj = datetime.datetime.strptime(dosage_time, "%H:%M")

        # Convert datetime object to AM/PM format
        dosage_time_obj_am_pm = dosage_time_obj.strftime("%I:%M %p")

        datetime_to_day = get_date_description(dosage_datetime)

        custom_message_1 = "Hi {}, Have you taken your medicine {} , Prescribed @{} , {}".format(patient_name, medicine_name, dosage_time_obj_am_pm, datetime_to_day )
        custom_message_2 = "Glad to Know that !! Did you took medicine as instructed - {}".format(dosage_instructions)

        current_dosage_tuple = (schedule_id, mobile_number, custom_message_1, custom_message_2)
        lst_reminder_messages.append(current_dosage_tuple)
        break

    return lst_reminder_messages
    

# Update the Medicine Schedule Based on Patient Response
def update_medicine_reminders(medicine_schedule_file_path, lst_reminder_response):
    # Load existing DataFrame or create a new one if it doesn't exist
    # medicine_schedule_df = pd.read_csv(medicine_schedule_file_path)
    medicine_schedule_df = medicine_schedule_file_path.copy()

    # Find the row with the matching s_id and update the columns
    for row in lst_reminder_response:
        s_id, response, instruction_response = row
        mask = medicine_schedule_df['schedule_id'] == s_id
        medicine_schedule_df.loc[mask, 'medicine_response'] = response
        instruction_response = "NA" if instruction_response is None else instruction_response
        medicine_schedule_df.loc[mask, 'instruction_response'] = instruction_response
        # print(medicine_schedule_df.loc[mask])

    # Save the updated DataFrame to a CSV file
    medicine_schedule_df.to_csv(medicine_schedule_file_path_temp, index=False)
    

# update_medicine_reminders([(11,"No", None), (12,"Yes", "Yes")])
# fetch_medicine_reminders

def read_prescription(prescription_df=None):
    prescription_df = pd.read_csv(os.path.join(data_dir,'prescription.csv'))
    medicine_schedule_df = pd.read_csv(os.path.join(data_dir,'medicine_schedule.csv'))

    max_schedule_id = medicine_schedule_df['schedule_id'].max()
    if pd.isna(max_schedule_id):
        max_schedule_id=0

    medicine_schedule_columns = list(medicine_schedule_df.columns)

    print('Max Schedule :', max_schedule_id)
    print(medicine_schedule_columns)
    # Create an empty DataFrame for the new data
    new_medicine_schedule_df = pd.DataFrame(columns=medicine_schedule_columns)

    # Iterate over each row in the input data
    for index, row in prescription_df.iterrows():
        prescription_date = pd.to_datetime(row['prescription_date'])
        number_of_days = row['number_of_days']
        morning = row['morning']
        afternoon = row['afternoon']
        evening = row['evening']
        time_intervals = []

        if morning == 1:
            time_intervals.append('09:00')
        if afternoon == 1:
            time_intervals.append('13:00')
        if evening == 1:
            time_intervals.append('22:00')

        # Generate schedule entries for each day and time interval
        for day in range(number_of_days):
            for time in time_intervals:
                schedule_id = len(new_medicine_schedule_df) + 1
                patient_id = row['patient_id']
                date = (prescription_date + pd.DateOffset(days=day)).strftime('%Y-%m-%d')
                medicine_name = row['medicine_name']
                symptoms = row['symptoms']
                instructions = row['instructions']
                medicine_response = ''
                instruction_response = ''

                # Append the schedule entry to the output DataFrame
                schedule_entry = pd.DataFrame({'schedule_id': max_schedule_id+schedule_id,
                                                'patient_id': patient_id,
                                                'date': date,
                                                'time': time,
                                                'medicine_name': medicine_name,
                                                'symptoms': symptoms,
                                                'instructions': instructions,
                                                'medicine_response': medicine_response,
                                                'instruction_response': instruction_response},
                                            index=[0])
                new_medicine_schedule_df = pd.concat([new_medicine_schedule_df, schedule_entry], ignore_index=True)

    concatenated_df = pd.concat([medicine_schedule_df, new_medicine_schedule_df], ignore_index=True)
    concatenated_df.to_csv(medicine_schedule_file_path_temp, index=None)