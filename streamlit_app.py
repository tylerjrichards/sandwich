import os

import pandas as pd
import plotly.express as px
import streamlit as st
from elosports.elo import Elo

st.image("sandwich.png")
#write out all the files in the directory
for dirname, _, filenames in os.walk('.'):
    for filename in filenames:
        st.write(os.path.join(dirname, filename))

st.subheader("Vote for your favorite sandwich!")
st.write(
    """Welcome to the SF Sandwich Showdown! We will be
    rating the best sandwiches in SF. Each round, you will be presented with two
    sandwiches. Vote for your favorite sandwich and record your results in this
    app. The results will be displayed at the end of the tournament."""
)
st.write("Made with love by [Tyler Richards](https://tylerjrichards.com)")
try:
    sandwich_rounds = pd.read_csv("sandwich_pairings.csv")
except:
    st.warning("Please head over to the sandwich setup app on sidebar first!")
    st.stop()
sandwich_rounds["Pairing 1 Winner?"] = False

# check if sandwich results.csv exists
preprepared_results = False
try:
    sandwich_results = pd.read_csv("sandwich_results.csv")
    preprepared_results = True
except:
    pass


# makes a base dataframe with the same columns as the sandwich pairings

base_dataframe = pd.DataFrame(
    columns=["Round", "Attendee", "Pairing 1", "Pairing 2", "Pairing 1 Winner?"]
)
for i in range(sandwich_rounds["Round"].max()):
    if preprepared_results == False:
        new_df = sandwich_rounds[sandwich_rounds["Round"] == i + 1]
        st.subheader(":balloon: Round " + str(i + 1) + " :balloon:")
        edited_df = st.data_editor(new_df)
        base_dataframe = pd.concat([base_dataframe, edited_df], ignore_index=True)
    else:
        new_df = sandwich_results[sandwich_results["Round"] == i + 1]
        st.subheader(":balloon: Round " + str(i + 1) + " :balloon:")
        edited_df = st.data_editor(new_df)
        base_dataframe = pd.concat([base_dataframe, edited_df], ignore_index=True)

st.subheader("🎉 Combined Results: 🎉")
st.data_editor(base_dataframe, num_rows="dynamic")
if st.button("Save Results"):
    base_dataframe.to_csv("sandwich_results.csv", index=False)
if st.button("Clear Results"):
    os.remove("sandwich_results.csv")


password = st.text_input("Enter the password to see the results", type="password")
if password != "sandwich":
    st.stop()

st.subheader(":sandwich: Sandwich Rating Results :sandwich:")
st.write("The results are in! Here are the final ratings for each sandwich.")


eloLeague = Elo(k=20)

unique_vals = pd.unique(base_dataframe[["Pairing 1", "Pairing 2"]].values.ravel("K"))


for i in unique_vals:
    eloLeague.addPlayer(i)


def update_elo(df):
    for i in range(len(df)):
        if df["Pairing 1 Winner?"][i] == True:
            eloLeague.gameOver(
                winner=df["Pairing 1"][i], loser=df["Pairing 2"][i], winnerHome=True
            )
        else:
            eloLeague.gameOver(
                winner=df["Pairing 1"][i], loser=df["Pairing 2"][i], winnerHome=True
            )


update_elo(base_dataframe)
rating_df = pd.DataFrame.from_dict(
    eloLeague.ratingDict, orient="index", columns=["Rating"]
).reset_index()
rating_df.columns = ["Sandwich Shop", "Rating"]
final_graph = px.bar(rating_df, x="Sandwich Shop", y="Rating")
# change y axis to be between 1300 and 1700
final_graph.update_layout(yaxis_range=[1350, 1650])
# order the x axis by rating
final_graph.update_xaxes(
    categoryorder="array",
    categoryarray=rating_df.sort_values(by="Rating", ascending=False)["Sandwich Shop"],
)
st.plotly_chart(final_graph)
