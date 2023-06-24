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

#using elo sports
from elosports.elo import Elo

eloLeague = Elo(k = 20)
eloLeague.addPlayer('BLT')
eloLeague.addPlayer('Grilled Cheese')
eloLeague.addPlayer('Peanut Butter & Jelly')
eloLeague.addPlayer('Tuna Salad')

#function to update elo scores
def update_elo(df):
    for i in range(len(df)):
        if df['Sandwich One Victory?'][i] == True:
            eloLeague.gameOver(winner=df['Sandwich One'][i], loser=df['Sandwich Two'][i], winnerHome=True)
        else:
            eloLeague.gameOver(winner=df['Sandwich Two'][i], loser=df['Sandwich One'][i], winnerHome=True)

#update elo scores
update_elo(edited_df)
st.write(eloLeague.ratingDict)
st.stop()
elo_scores = update_elo(edited_df)
st.write(elo_scores)