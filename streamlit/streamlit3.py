# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from soccerplots.radar_chart import Radar
from sklearn.metrics.pairwise import cosine_similarity
from math import pi
import numpy as np

st.set_page_config(
    page_title="football Player Recommendation System ",
    menu_items={"Get Help":"https://github.com/bakindi",
                "About":"for more information"+"https://github.com/bakindi"
                })

st.set_option('deprecation.showPyplotGlobalUse', False)

# Load your dataset
@st.cache_data
def load_data():
    df = pd.read_csv('C:/Users/asus/Desktop/streamlit_recomendation/result.csv')
    return df

df = load_data()

# Function to recommend players
def recommend_players(player):
    # Calculate cosine similarity
    similarity = cosine_similarity(df.iloc[:, 2:], player)  # assuming the first two columns are player name and position
    df['similarity'] = similarity
    # Sort by similarity
    df_sorted = df.sort_values(by='similarity', ascending=False)
    # Return top 10 similar players
    return (df_sorted.head(11)).iloc[1:11,0:10]

# Function to create radar chart
#add ranges to list of tuple pairs
## range values
ranges = [(0,100), (0,100), (0,100), (0,100),
          (0,100), (0,100), (0,100), (0,100)]

a_values = []
b_values = []

def compparison_player (nama1, nama2) :
    params = list(df.columns)

    for x in range(len(df['player'])):
        if df['player'][x] == nama1:
          pos = 0
          params = params[2:-1]
          a_values = df.iloc[x].values.tolist()

        if df['player'][x] == nama2:
            b_values = df.iloc[x].values.tolist()

    a_values = a_values[2:]
    b_values = b_values[2:]

    a_values_ = []
    a_values_.append((a_values[0]*100)/0.5)
    a_values_.append((a_values[1]*100)/0.6)
    a_values_.append((a_values[2]*100)/0.4)
    a_values_.append((a_values[3]*100)/0.6)
    a_values_.append((a_values[4]*100)/0.4)
    a_values_.append((a_values[5]*100)/0.6)
    a_values_.append((a_values[6]*100)/0.4)
    a_values_.append((a_values[7]*100)/0.7)

    b_values_ = []
    b_values_.append((b_values[0]*100)/0.5)
    b_values_.append((b_values[1]*100)/0.6)
    b_values_.append((b_values[2]*100)/0.4)
    b_values_.append((b_values[3]*100)/0.6)
    b_values_.append((b_values[4]*100)/0.4)
    b_values_.append((b_values[5]*100)/0.6)
    b_values_.append((b_values[6]*100)/0.4)
    b_values_.append((b_values[7]*100)/0.7)

    print (x)
    values = [a_values_,b_values_]
    #title

    title = dict(
    title_name=nama1,
    title_color = 'red',
    subtitle_color = 'red',
    title_name_2=nama2,
    title_color_2 = 'blue',
    subtitle_color_2 = 'blue',
    title_fontsize = 18,
    subtitle_fontsize=15)

    radar = Radar(range_fontsize=9)

    fig,ax = radar.plot_radar(ranges=ranges,params=params,values=values,
                         radar_color=['red','blue'],
                         alphas=[.75,.6],title=title,
                         compare=True)

# Streamlit app
st.title('Football Player Recommendation System')

# Sidebar with project information
st.sidebar.title('About the Project')
st.sidebar.text('This page is an exemplary player')
st.sidebar.text('recommendation system that recommends')
st.sidebar.text('players playing in the 5 big leagues')
st.sidebar.text('of Europe in the 2019-20 season,')
st.sidebar.text('it was developed by jr football')
st.sidebar.text('data scientist battal bakindi.')
st.sidebar.text('the way it works; 1) You can ask')
st.sidebar.text('the system to suggest similar')
st.sidebar.text('real football players by entering')
st.sidebar.text('the skills of your dream football')
st.sidebar.text('player you need. 2) you can see similar')
st.sidebar.text('football players by choosing a real')
st.sidebar.text('football player whose skills you like.')

# User inputs
st.subheader('Create your dream football player or select a real player')
method = st.radio('Choose a method', ('Create a player', 'Select a player'))

if method == 'Create a player':
    passes = st.slider('Passes', min_value=0, max_value=100)
    creativity = st.slider('Creativity', min_value=0, max_value=100)
    aerials = st.slider('Aerials', min_value=0, max_value=100)
    shots = st.slider('Shots', min_value=0, max_value=100)
    defensive = st.slider('Defensive', min_value=0, max_value=100)
    offensive = st.slider('Offensive', min_value=0, max_value=100)
    dribbling = st.slider('Dribbling', min_value=0, max_value=100)
    physical = st.slider('Physical', min_value=0, max_value=100)

    # Create synthetic player
    synthetic_player = pd.DataFrame([[passes, creativity, aerials, shots, defensive, offensive, dribbling, physical]], 
                                    columns=df.columns[2:])  # assuming the first two columns are player name and position

    # Button to run recommendation
    if st.button('Recommend Players'):
        recommendations = recommend_players(synthetic_player)
        st.dataframe(recommendations)

elif method == 'Select a player':
    player_name = st.selectbox('Select a player', df['player'].unique())
    player = df[df['player'] == player_name].iloc[:, 2:]

    # Button to run recommendation
    if st.button('Recommend Players'):
        recommendations = recommend_players(player)
        recom = recommendations["player"].unique()
        st.dataframe(recommendations)
        st.pyplot(compparison_player(player_name, recom[0] ))
