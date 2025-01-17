import streamlit as st
import re
import requests
import time  # To generate unique form keys

WEBHOOK_URL = st.secrets['webhook']['WEBHOOK_URL']

def email_is_valid(address):
    email_re = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_re, address) is not None

def contact_form():
    with st.form('Contact Me'):
        name = st.text_input('Name')
        email = st.text_input('Email')
        message = st.text_area('Your Message')  # Changed to `text_area` for longer messages
        submit = st.form_submit_button('Submit')

        if submit:
            # Validate inputs
            if not WEBHOOK_URL:
                st.error('Email service error. Please try again later.', icon='📧')
                return
            if not name.strip():
                st.error('Please provide your name.', icon='📛')
                return
            if not email.strip():
                st.error('Please provide a valid email address.', icon='📨')
                return
            if not email_is_valid(email):
                st.error('Invalid email format. Please provide a valid email address.', icon='📨')
                return
            if not message.strip():
                st.error('Please include a message.', icon='🗨️')
                return

            # Prepare and send the payload
            data = {'email': email, 'name': name, 'message': message}
            st.write("Message Preview: ", data)
            
            try:
                response = requests.post(WEBHOOK_URL, json=data)
                if response.status_code == 200:
                    st.success('Thanks for your message!', icon='🚀')
                else:
                    st.error(f"Error sending message: {response.status_code}. Details: {response.text}", icon='😱')
            except Exception as e:
                st.error(f"An error occurred: {str(e)}", icon='😱')
