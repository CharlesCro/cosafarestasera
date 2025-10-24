# Standard Libraries
import datetime
import time
import os
import ast


# Non-Standard Libraries
import xyzservices.providers as xyz
from dotenv import load_dotenv
import folium
import streamlit as st

# Custom Modules
from concierge.agent import invoke
from config.settings import get_api_key
from utils.helpers import init_session_state
from ui.components import load_header, load_sidebar, load_events

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
        # Interests component
        st.session_state.interests = st.multiselect(
            '**Please add your interests**',
            ['Art', 'Jazz', 'Farmer\'s Market', 'Theatre', 'Hiking',' Disco'],
            max_selections = 20,
            accept_new_options = True
        )

        st.divider()

        st.header('', divider = 'violet')
        st.session_state.location = st.text_input('**Enter Location**', width = 250, placeholder = 'e.g., Firenze, Italia')

        today = datetime.datetime.now()

        if st.toggle('Select Multiple Days'):
            st.session_state.range_on = True
        else:
            st.session_state.range_on = False

        if st.session_state.range_on:
            st.session_state.date_range = st.date_input('**Enter date**', (today, datetime.date(today.year + 1, today.month, today.day)), format="YYYY.MM.DD")
        else:
            st.session_state.date_range = st.date_input('**Enter date**', format="YYYY.MM.DD")

        

        if st.session_state.interests:

            if st.button('Search', type = 'primary'):
                st.session_state.search = True
        else:
            st.info('Please Add Interests to Begin Search')
        
        st.header('', divider = 'violet')
        
        
            

    with right:
        if st.session_state.search:
            st.session_state.search = False
            prompt = f"""
                        Conduct a google search of an area to help the user find an activity/event based on their provided interests below. Ensure the events are relevant and occur on the day at the place provided:
                        User Interests: {st.session_state.interests}
                        Date Range: {st.session_state.date_range}
                        Location: {st.session_state.location}
                        """
                
            with st.spinner('Searching...', show_time = True):
                agent_response = invoke(prompt)
                # agent_response = run_adk_sync(adk_runner, current_session_id, prompt)
                
                st.toast("Hip!")
                time.sleep(0.5)
                st.toast("Hip!")
                time.sleep(0.5)
                st.toast("Hooray!", icon="🎉")

            st.session_state.agent_response = ast.literal_eval(agent_response.strip().strip('```json').strip('```').strip())

        if st.session_state.agent_response:
            load_events(st.session_state.agent_response)
            
        if st.session_state.agent_response:
            st.info('Map Test Version (Not Complete)')
            # DISPLAY MAP DEFAULT LOCATION
            map = folium.Map(location = [41.8719, 12.5674], tiles = xyz.Jawg.Matrix(accessToken = os.getenv('JAWG_API_KEY') , variant = "jawg-matrix"), zoom_control = False, zoom_start = 11)

            # MAP MARKERS
            folium.CircleMarker(location=[41.8719, 12.5674],
                            radius=10,
                            color="mediumslateblue",
                            stroke=False,
                            fill=True,
                            fill_opacity=1,
                            opacity=1,
                            popup="Roma, IT").add_to(map)

            st.components.v1.html(folium.Figure().add_child(map).render(), height=500)
            
        else:
            st.info("Press *Search* for assistance")










    