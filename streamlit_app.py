import pandas as pd
import streamlit as st

st.image('sandwich.png')

st.subheader('Vote for your favorite sandwich!')

#make dataframe with sandwich names and votes
sandwiches = ['BLT', 'Grilled Cheese', 'Peanut Butter & Jelly', 'Tuna Salad']
votes = [False, False, False, False]
#randomly order sandwiches into new list

sandwiches_2 = sandwiches.copy()
import random

random.seed(4)
random.shuffle(sandwiches_2)

df = pd.DataFrame({'Sandwich One': sandwiches, 'Sandwich Two': sandwiches_2, 'Sandwich One Victory?': votes})

st.subheader('Round One')
edited_df = st.data_editor(df)
