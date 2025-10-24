# Non-Standard Libraries
import streamlit as st
import pandas as pd

# Custom Modules
from config.settings import MESSAGE_HISTORY_KEY
from services.concierge_service import run_adk_sync

def login_screen():
    '''Google OAuth'''
    st.header('Welcome to LocaleWeb')
    if st.button("Log in with Google"):
        st.login()

def load_events(events):
    df = pd.DataFrame(events)

    # Prepare data for map: split coordinates into lat/lon
    map_df = df.copy()
    map_df[['lat', 'lon']] = map_df['event_location'].str.split(', ', expand=True).astype(float)
    
    st.subheader(f"📍 Map View ({len(map_df)} Events)")
    st.map(map_df[['lat', 'lon']], zoom=10, use_container_width=True)
    st.divider()

    # Iterate through the filtered events and display them
    for _, event in df.iterrows():
        # Use st.container to create a distinct, visually separated card for each event
        # Add a border using markdown/CSS injection for a cleaner look
        with st.container(border=True):
            
            # 1. Title and Category
            col1, col2 = st.columns([4, 1])
            with col1:
                st.subheader(event['event_name'])
            with col2:
                # Use st.badge for a highlighted category
                st.caption(f"Category: **{event['event_category']}**")


            # 2. Key Details (Date and Location)
            # Use another set of columns for side-by-side details
            date_col, location_col = st.columns(2)
            
            with date_col:
                st.markdown(f"🗓️ **When:** {event['event_date']}")
            
            with location_col:
                # Link to Google Maps (approximate location using coordinates)
                lat, lon = event['event_location'].split(', ')
                map_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                st.markdown(f"🗺️ **Where:** [{event['event_location']}]({map_link})")


            # 3. Description (using expander for tidiness)
            with st.expander("Read Full Description"):
                st.markdown(event['event_description'])

            # 4. Source Link
            st.markdown(f"[Source Link]({event['event_source_link']})")
        
        # Add a small vertical space after each card (optional, as st.container adds margin)
        st.write("")

def load_header():
    '''Title & Logo'''
    col1, col2, _ = st.columns([1, 5, 14])
    col1.image('ui/assets/logo_locale.jpg', width = 75)
    col2.title(':blue[blue]print.') # Main title of the app.
    st.caption('Itinerary helper, designing the schematics for your outing.') # Descriptive text.

def load_sidebar():
    # User Info (suppressed for localhost testing)
    
    with st.sidebar:
        if not st.user.is_logged_in:
            if st.button("Log in with Google"):
                st.login()
            st.stop()

        if st.button("Log out"):
            st.logout()
        st.markdown(f"Welcome, {st.user.name}")
    

    with st.sidebar:
        st.divider()

        st.sidebar.write(
            '''
            :orange[Developed] :orange[by:]
            Charles Crocicchia & Alex Fratoni

            '''
        )
        """
        st.write()
        st.header('Speak with the :violet[Architect]', divider = 'violet')
        
        
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
                    agent_response = run_adk_sync(adk_runner, current_session_id, prompt + f'''
                            Interests: {st.session_state.interests}
                            Location: {st.session_state.location}
                            Date: {st.session_state.date_range}
                            ''') # Call the synchronous ADK runner.
                    print(f"DEBUG UI: Received response from ADK: {agent_response[:50]}...")
                    message_placeholder.markdown(agent_response) # Update the placeholder with the final response.
            
            # Append assistant's response to history.
            st.session_state[MESSAGE_HISTORY_KEY].append({'role': 'assistant', 'content': agent_response})
            """
    

