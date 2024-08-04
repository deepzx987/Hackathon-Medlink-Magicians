# import streamlit as st
# from streamlit.components import v1

# st.title('Content inside tabs jitters on first load')
# t1, t2, t3 = st.tabs(['First tab', 'Second tab', 'Third tab'])

# t1.header('This content is inside the first tab')
# t2.header('This content is inside the second tab')
# t3.header('This content is inside the third tab')

# v1.html("""
# <script>
# function checkElements() {
#     const tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"] p');
#     const tab_panels = window.parent.document.querySelectorAll('div[data-baseweb="tab-panel"]');

#     if (tabs && tab_panels) {

#         tabs.forEach(function (tab, index) {
#             const tab_panel_child = tab_panels[index].querySelectorAll("*");

#             function set_visibility(state) {
#                 tab_panels[index].style.visibility = state;
#                 tab_panel_child.forEach(function (child) {
#                     child.style.visibility = state;
#                 });
#             }

#             tab.addEventListener("click", function (event) {
#                 set_visibility('hidden')

#                 let element = tab_panels[index].querySelector('div[data-testid="stVerticalBlock"]');
#                 let main_block = window.parent.document.querySelector('section.main div[data-testid="stVerticalBlock"]');
#                 const waitMs = 1;

#                 function waitForLayout() {
#                     if (element.offsetWidth === main_block.offsetWidth) {
#                         set_visibility("visible");
#                     } else {
#                         setTimeout(waitForLayout, waitMs);
#                     }
#                 }

#                 waitForLayout();
#             });
#         });
#     } else {
#         setTimeout(checkElements, 100);
#     }
# }

# checkElements()
# </script>
# """, height=0)



import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from ecg import *
from GPS import *

def generate_graph():
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)

    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Sine Wave')
    plt.grid(True)

    return plt

def main():
    tab1, tab2 = st.tabs(["ECG Rhythm Prediction", "Patient Tracking"])

    active_tab = st.sidebar.radio("Select Tab", tabs)

    if active_tab == "Tab 1":
        # Display Matplotlib graph in Tab 1
        ECG_Rhythm_Prediction()

    elif active_tab == "Tab 2":
        # Display some other content in Tab 2
        st.write("This is Tab 2")
        geolocation_analysis()

if __name__ == "__main__":
    main()
