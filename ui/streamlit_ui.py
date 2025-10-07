import datetime
import streamlit as st
from services.adk_service import initialize_adk, run_adk_sync
from config.settings import MESSAGE_HISTORY_KEY, get_api_key


def add_new_field():
    """Callback function to increase the number of input fields."""
    st.session_state.interests_count += 1
    # When a new field is added, we immediately rerun the app

def process_form_submission():
    """Callback function to process all inputs and store unique interests."""
    
    # 1. Get all current interest values from session state
    current_inputs = []
    for i in range(st.session_state.interests_count):
        key = f'interest_input_{i}'
        # Get the value, strip whitespace, and convert to lowercase for case-insensitive checking
        interest = st.session_state[key].strip().lower()
        if interest: # Only add non-empty strings
            current_inputs.append(interest)
    
    # 2. Add only new, unique interests to the main list
    for new_interest in current_inputs:
        if new_interest not in st.session_state.interest_values:
            st.session_state.interest_values.append(new_interest)

    st.success("Interests added successfully! Check the list below.")
    # Optional: Reset the input count after submission if you want a fresh form
    st.session_state.interests_count = 1
    for i in range(len(current_inputs)):
        key = f'interest_input_{i}'
        if key in st.session_state:
            del st.session_state[key]

def run_streamlit_app():
    '''
    Sets up and runs the Streamlit web application for the ADK chat assistant.
    '''
    if 'interests_count' not in st.session_state:
        st.session_state.interests_count = 1  # Start with one input box

    if 'interest_values' not in st.session_state:
        st.session_state.interest_values = [] # Final list to store unique interests
    if 'agent_response' not in st.session_state:
        st.session_state.agent_response = None

    st.set_page_config(page_title='CosaFareStasera', layout='wide') # Configures the browser tab title and page layout.
    st.title(':blue[Cosa]Fare:red[Stasera]') # Main title of the app.
    st.caption('Powered by ADK & Gemini') # Descriptive text.
    st.header('', divider = 'blue')
    api_key = get_api_key() # Retrieve the API key from settings.
    if not api_key:
        st.error('Action Required: Google API Key Not Found or Invalid! Please set GOOGLE_API_KEY in your .env file. ⚠️')
        st.stop() # Stop the application if the API key is missing, prompting the user for action.
    # Initialize ADK runner and session ID (cached to run only once).
    adk_runner, current_session_id = initialize_adk()
    
    # Display session ID for debugging purposes
    st.sidebar.title('Info')
    st.sidebar.divider()
    st.sidebar.info(
        '''
        This app allows users to search for things to do in the specified date, location
        and provide customized interests and hobbies for a tailored experience.


        ---

        :red[Coming Soon:] 
        
        - Better search results, better UI

        - Map

        - Chatbot

        ---

        :orange[Developed] :orange[by:]
        Charles Crocicchia & Alex Fratoni
        '''
    )

    print(f"DEBUG UI: Using ADK session ID: {current_session_id}")
    
    left, right = st.columns([1, 2], border = True)

   
    with left:
        st.session_state.location = st.text_input('Enter Location', width = 250, placeholder = 'e.g., Firenze, Italia')

        st.session_state.date_range = st.date_input('Enter date', format="MM.DD.YYYY")

        if st.session_state.interest_values:

            if st.button('What should I do tonight?', type = 'primary'):
                prompt = f"""
                        Conduct a google search of an area to help the user find an activity/event based on their provided interests below. Ensure the events are relevant and occur on the day at the place provided:
                        User Interests: {sorted(list(set(st.session_state.interest_values)))}
                        Date Range: {st.session_state.date_range}
                        Location: {st.session_state.location}
                        """
                
                with st.spinner('Searching...', show_time = True):
                    agent_response = run_adk_sync(adk_runner, current_session_id, prompt)

                    st.session_state.agent_response = agent_response
        else:
            st.info('Please Add Interests to Begin Search')

        st.header('', divider = 'red')
         # Create a container for the input fields and "add" button
        input_container = st.container()
        with input_container:
            # A button to add a new input field (uses a callback to update the count)
            st.button(":material/add: Add Field", on_click=add_new_field)

            # A Streamlit Form to batch the text inputs and submission button
            with st.form(key='interest_form'):
                st.subheader("Your Interests")
                
                # Loop to dynamically generate the required number of text input boxes
                for i in range(st.session_state.interests_count):
                    # IMPORTANT: A unique 'key' is required for every widget,
                    # especially in a loop, to store its value in st.session_state.
                    st.text_input(
                        f"Interest #{i + 1}", 
                        key=f'interest_input_{i}',
                        placeholder="e.g., Art, Jazz, Farmer's Markets"
                    )

                # The form submission button
                st.form_submit_button(
                    label='Submit All Interests', 
                    on_click=process_form_submission
                )


        ## Stored Interests

        if st.session_state.interest_values:
            # Convert the list to a set and back to a list just in case any duplicates slipped through,
            # then display them as a list of bullet points.
            unique_interests = sorted(list(set(st.session_state.interest_values)))
            st.write("Current unique interests:")
            st.markdown('\n'.join([f"- {i.title()}" for i in unique_interests]))

            st.session_state.interests = unique_interests
            
            # A button to clear the stored list of interests
            if st.button("Clear Saved Interests"):
                st.session_state.interest_values = []
                st.rerun()
        
            

    with right:
        if st.session_state.agent_response:
            st.markdown(agent_response)

    st.header('', divider = 'blue')



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