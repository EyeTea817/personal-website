import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

st.set_page_config(page_title="Page Title", layout="wide")

hide_streamlit_style = """
            <style>
                /* Hide the Streamlit header and menu */
                header {visibility: hidden;}
                /* Optionally, hide the footer */
                .streamlit-footer {display: none;}
                /* Hide your specific div class, replace class name with the one you identified */
                .st-emotion-cache-uf99v8 {display: none;}
                .stAppToolbar {display: none;}
                #GithubIcon { visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)


st.title('Ian Temchin')



# --- PAGES ---
home = st.Page(
    page = 'views/about_me.py',
    title= 'Resume',
    icon=':material/account_circle:',
    default=True,
)

poker = st.Page(
    page = 'views/poker.py',
    title = 'Poker Statistics',
    icon = ':material/playing_cards:'
)

portfolio1 = st.Page(
    page = 'views/portfolio1.py',
    title= 'Groundwater Monitoring Simulation',
    icon=':material/bar_chart:',
)

portfolio2 = st.Page(
    page = 'views/portfolio2.py',
    title= 'Sales Dashboard',
    icon=':material/bar_chart:',
)

# --- SIDEBAR NAVIGATION ---
pg = st.navigation(
    {'About Me': [home, poker],
     'Projects': [portfolio2]}
)

st.sidebar.text('© 2025 Ian Temchin. All rights reserved.')

pg.run()

