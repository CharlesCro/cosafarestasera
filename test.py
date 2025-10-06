import streamlit as st
import pandas as pd

st.title(":blue[Cosa] :green[Fare] :red[Stasera]")

st.divider()

def search(interests):
    if interests:
        st.write('Your saved interests:')

        for interest in interests:
            st.write(f'- {interest}')
    
    else:
        st.write('No interests registered yet.')

if 'interests' not in st.session_state:
    st.session_state['interests'] = []


if prompt := st.chat_input("Enter a new interest at any time to update your preferences"):

    st.session_state['interests'].append(prompt)

    st.chat_message('assistant').write(f'{prompt} registered as interest.')


if st.button('Search'):
    search(st.session_state.get('interests'))
