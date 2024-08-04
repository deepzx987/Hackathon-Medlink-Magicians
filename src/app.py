import streamlit as st
import os
from pathlib import Path
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space



# sys.path.append('data')
st.set_page_config(page_title="Medlink Magicians",layout="wide")

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


#st.title("TableTraverse")
st.markdown('<h1 class="title">Medlink Magicians</h1>', unsafe_allow_html=True)

#st.sidebar.write('## Document Summarizer settings')
# st.write("## CSR")
#uploaded_file = st.sidebar.file_uploader("Upload Document", type=['pdf'])


options = ["","AWS","AZURE"]
# Display the dropdown menu
selected_option = st.sidebar.selectbox("Cloud Type", options,index=0)

# add sidebar
#st.sidebar.subheader("Settings")
st.sidebar.markdown('<h1 class="subheader">Settings</h1>', unsafe_allow_html=True)

# Temperature
temperature = st.sidebar.slider("Creativity", 0.0, 2.0, 0.5, 0.1,help='**Creativity** determines how much creative the model will be.')

# Top-p
top_p = st.sidebar.slider("Threshold", 0.0, 1.0, 0.5, 0.1,help="**Threshold** determines the diversity in choice of words for generating the summary.")

# Max tokens till 2048
max_tokens = st.sidebar.slider("Summary Length", 256, 2048, 1024, 1,help='**Summary Length** determines the token size which helps generate complete summary. Higher Summary length will tend to generate long and elaborated summary. Use recommended  summary length to begin with.')


st.sidebar.markdown('<h1 class="subheader">About</h1>', unsafe_allow_html=True)
st.sidebar.info(
    '''This application is built with the help of open source LLM and 
    it is capable of answering questions regarding Enterprise Cloud
        '''
    )

with st.sidebar:
    st.write('Made with ❤️ by [JAIGPT]')


# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm JaiGPT EA cloud chat, How may I help you?"]
## past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

if "history" not in st.session_state:
    st.session_state.history = []

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()


# User input
## Function for taking user provided prompt as input

def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text
## Applying the user input box
with input_container:
    user_input = get_text()

st.session_state.history.append({"message": user_input, "is_user": True})

def clear_chat() -> None:
    st.session_state.generated = []
    st.session_state.past = []
    st.session_state.history = []
    st.session_state.user_input = ""

st.button(label="clear chat history", on_click=clear_chat)

response_container = st.container()


def generate_response(prompt):

    response = "Ruko zara sabar karo"  # chatbot.chat(prompt)
    return response


with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

