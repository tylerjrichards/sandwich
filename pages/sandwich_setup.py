import streamlit as st

st.title('Sandwich Setup')

sandwich_options = ['Hazel', 'El Metate', "Lucinda's", 'Thorough Bread', 'Le Sandwich', "Turner's", 'RT Rotisserie', 'Medialuna', 'Tartine']
attendees = ['Tenn', 'Connie', 'Gatsby', 'Tanzeela', 'Lisa', 'Ashni', 'Noah', 'Serin', 'Kishan', 'Ron', 'Shelby', 'Nikhil', 'Tyler']
sandwiches = st.multiselect(options=sandwich_options, label='Select the available sandwiches', default=sandwich_options)
attendee_number = st.number_input('Select the number of attendees', 1, 20, 10)
round_number = st.number_input('Select the number of rounds', 0, 4, 2)

import itertools
import random
import string

import pandas as pd


def remove_digits(s: str):
    return s.translate(str.maketrans("", "", string.digits))

def generate_sandwich_pairings(sandwich_options: list, attendees: list, rounds: int):
    sandwich_quarters = [s + str(i) for s in sandwich_options for i in range(1, 9)]
    pairings = []
    sandwich_combinations = list(itertools.combinations(sandwich_quarters, 2))

    for r in range(rounds):
        random.shuffle(sandwich_combinations)
        round_pairings = [sandwich_combinations[i:i+1] for i in range(0, len(attendees), 1)]
        sandwich_combinations = [c for c in sandwich_combinations if not any(c in p for p in round_pairings)]
        pairings.append(round_pairings)

    return pairings

pairings = generate_sandwich_pairings(sandwich_options, attendees, round_number)


data = []

for r, round_pairings in enumerate(pairings, start=1):
    for i, attendee_pairings in enumerate(round_pairings, start=1):
        data.append([r, attendees[i-1]] + [remove_digits(p) for p in attendee_pairings[0]])

df = pd.DataFrame(data, columns=['Round', 'Attendee', 'Pairing 1', 'Pairing 2'])
if any(df['Pairing 1'] == df['Pairing 2']):
    st.error('Pairing 1 cannot be the same as Pairing 2')
    st.experimental_rerun()
edited_df = st.data_editor(df, use_container_width=True)

#if for any row, pairing 1 is the same as pairing 2, then regenerate pairings



st.divider()
st.subheader('Satisfied with the pairings?')
if st.button('Save Pairings'):
    edited_df.to_csv('sandwich_pairings.csv', index=False)
if st.button('Regenerate Pairings'):
    st.experimental_rerun()

