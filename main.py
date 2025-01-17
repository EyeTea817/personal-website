import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

st.set_page_config(layout='wide')
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
pg.run()

