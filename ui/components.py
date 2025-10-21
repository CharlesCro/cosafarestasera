# Non-Standard Libraries
import streamlit as st

# Custom Modules
from config.settings import MESSAGE_HISTORY_KEY
from services.concierge_service import run_adk_sync

def login_screen():
    '''Google OAuth'''
    st.header('Welcome to LocaleWeb')
    if st.button("Log in with Google"):
        st.login()

def load_header():
    '''Title & Logo'''
    col1, col2, _ = st.columns([1, 5, 14])
    col1.image('ui/assets/logo_locale.jpg', width = 75)
    col2.title(':blue[blue]print.') # Main title of the app.
    st.caption('Itinerary helper, designing the schematics for your outing.') # Descriptive text.

def load_sidebar(adk_runner, current_session_id):
    # User Info (suppressed for localhost testing)
    '''
    with st.sidebar:
        if not st.user.is_logged_in:
            if st.button("Log in with Google"):
                st.login()
            st.stop()

        if st.button("Log out"):
            st.logout()
        st.markdown(f"Welcome, {st.user.name}")
    '''

    with st.sidebar:
        st.divider()

        st.sidebar.write(
            '''
            :orange[Developed] :orange[by:]
            Charles Crocicchia & Alex Fratoni

            '''
        )

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
        

