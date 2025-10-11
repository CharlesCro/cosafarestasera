import datetime
import os
import xyzservices.providers as xyz

from dotenv import load_dotenv
import folium
import streamlit as st

from services.concierge_service import initialize_adk, run_adk_sync
from config.settings import MESSAGE_HISTORY_KEY, get_api_key

load_dotenv()

def login_screen():
    st.header('Welcome to LocaleWeb')
    if st.button("Log in with Google"):
        st.login()

def run_streamlit_app():
    '''
    Sets up and runs the Streamlit web application for the ADK chat assistant.
    '''
    
    if 'interests' not in st.session_state:
        st.session_state.interests = []  # Start with one input box
    if 'agent_response' not in st.session_state:
        st.session_state.agent_response = None
    if 'range_on' not in st.session_state:
        st.session_state.range_on = False
    if 'search' not in st.session_state:
        st.session_state.search = False

    st.set_page_config(page_title='Locale', layout='wide') # Configures the browser tab title and page layout.
    
    col1, col2, _ = st.columns([1, 3, 14])
    col1.image('ui/assets/logo_locale.jpg', width = 75)
    col2.title('LocaleWeb') # Main title of the app.
    st.caption('Powered by ADK & Gemini') # Descriptive text.
    

    api_key = get_api_key() # Retrieve the API key from settings.
    if not api_key:
        st.error('Action Required: Google API Key Not Found or Invalid! Please set GOOGLE_API_KEY in your .env file. ⚠️')
        st.stop() # Stop the application if the API key is missing, prompting the user for action.
    # Initialize ADK runner and session ID (cached to run only once).
    adk_runner, current_session_id = initialize_adk()

    # User Info
    with st.sidebar:
        if not st.user.is_logged_in:
            if st.button("Log in with Google"):
                st.login()
            st.stop()

        if st.button("Log out"):
            st.logout()
        st.markdown(f"Welcome, {st.user.name}")

    st.sidebar.divider()
    
    # Website Info
    st.sidebar.write(
        '''
        :orange[Developed] :orange[by:]
        Charles Crocicchia & Alex Fratoni

        This app allows users to search for things to do in the specified date, location
        and provide customized interests and hobbies for a tailored experience.

        Potential App Names: "When & Where" (WW for short), "Findr" (Too much like Grindr?), "vibe."
           
        
        '''
    )

    # Date & Location settings
    with st.sidebar:
        st.header('', divider = 'violet')
        st.session_state.location = st.text_input('**Enter Location**', width = 250, placeholder = 'e.g., Firenze, Italia')

        today = datetime.datetime.now()

        if st.toggle('Select Multiple Days'):
            st.session_state.range_on = True
        else:
            st.session_state.range_on = False

        if st.session_state.range_on:
            st.session_state.date_range = st.date_input('**Enter date**', (today, datetime.date(today.year + 1, today.day, today.month)), format="MM.DD.YYYY")
        else:
            st.session_state.date_range = st.date_input('**Enter date**', format="MM.DD.YYYY")

        

        if st.session_state.interests:

            if st.button('Search', type = 'primary'):
                st.session_state.search = True
        else:
            st.info('Please Add Interests to Begin Search')
        
        st.header('', divider = 'violet')

        


        

    print(f"DEBUG UI: Using ADK session ID: {current_session_id}")
    
    left, right = st.columns([1, 2], border = True)

    with left:
        st.session_state.interests = st.multiselect(
            '**Please add your interests**',
            ['Art', 'Jazz', 'Farmer\'s Market', 'Theatre', 'Hiking',' Disco'],
            max_selections = 20,
            accept_new_options = True
        )

        st.divider()
        
        if st.session_state.search:
            st.session_state.search = False
            prompt = f"""
                        Conduct a google search of an area to help the user find an activity/event based on their provided interests below. Ensure the events are relevant and occur on the day at the place provided:
                        User Interests: {st.session_state.interests}
                        Date Range: {st.session_state.date_range}
                        Location: {st.session_state.location}
                        """
                
            with st.spinner('Searching...', show_time = True):
                agent_response = run_adk_sync(adk_runner, current_session_id, prompt)
                import time
                st.toast("Hip!")
                time.sleep(0.5)
                st.toast("Hip!")
                time.sleep(0.5)
                st.toast("Hooray!", icon="🎉")

            st.session_state.agent_response = agent_response  

        if st.session_state.agent_response:
            st.markdown(st.session_state.agent_response)
            

    with right:
        
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
        st.info('Alpha Version', width = 120)











    '''
    # Initialize chat message history in Streamlit's session state if it doesn't exist.
    if MESSAGE_HISTORY_KEY not in st.session_state:
        st.session_state[MESSAGE_HISTORY_KEY] = []
    # Display existing chat messages from the session state.
    for message in st.session_state[MESSAGE_HISTORY_KEY]:
        with st.chat_message(message['role']): # Use Streamlit's chat message container for styling.
            st.markdown(message['content'])
    # Handle new user input.
    if prompt := st.chat_input('Enter message'):
        # Append user's message to history and display it.
        st.session_state[MESSAGE_HISTORY_KEY].append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)
        # Process the user's message with the ADK agent and display the response.
        with st.chat_message('assistant'):
            message_placeholder = st.empty() # Create an empty placeholder to update with the assistant's response.
            with st.spinner('Assistant is thinking...'): # Show a spinner while the agent processes the request.
                print(f"DEBUG UI: Sending message to ADK with session ID: {current_session_id}")
                agent_response = run_adk_sync(adk_runner, current_session_id, prompt) # Call the synchronous ADK runner.
                print(f"DEBUG UI: Received response from ADK: {agent_response[:50]}...")
                message_placeholder.markdown(agent_response) # Update the placeholder with the final response.
        
        # Append assistant's response to history.
        st.session_state[MESSAGE_HISTORY_KEY].append({'role': 'assistant', 'content': agent_response})
    '''