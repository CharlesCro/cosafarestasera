
# Non-Standard Libraries
from dotenv import load_dotenv
import streamlit as st

# Custom Modules
from config.settings import get_api_key
from utils.helpers import init_session_state
from ui.components import load_header, load_sidebar, load_left_column, load_right_column

# Import Environment Variables
load_dotenv()

def run_streamlit_app():
    '''
    Sets up and runs the Streamlit web application for the ADK chat assistant.
    '''
    
    # Initialize session state variables
    init_session_state()

    # Page Configuration
    st.set_page_config(page_title='Locale', layout='wide') # Configures the browser tab title and page layout.

    # Load header
    load_header()

    # Initialize ADK Session with API key
    api_key = get_api_key() # Retrieve the API key from settings.
    if not api_key:
        st.error('Action Required: Google API Key Not Found or Invalid! Please set GOOGLE_API_KEY in your .env file. ⚠️')
        st.stop() # Stop the application if the API key is missing, prompting the user for action.
    

    # Load sidebar (Login & info)
    load_sidebar()
    
    # <-- Main Page -->
    left, right = st.columns([1, 2], border = True)

    with left:
        load_left_column()


    with right:

        load_right_column()










    