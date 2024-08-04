from twilio.rest import Client
import streamlit as st

# Obtain account_sid, auth_token, Message, To Number, from_

client = Client(account_sid, auth_token)

def send_message(Message, To):
    client.messages.create(from_='asdfdasf', body=Message, to=To)
