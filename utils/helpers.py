# Non-Standard Libraries
import streamlit as st

def init_session_state():
    
    if 'interests' not in st.session_state:
        st.session_state.interests = []  # Start with one input box
    if 'agent_response' not in st.session_state:
        st.session_state.agent_response = None
    if 'range_on' not in st.session_state:
        st.session_state.range_on = False
    if 'search' not in st.session_state:
        st.session_state.search = False