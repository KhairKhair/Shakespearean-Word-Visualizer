import torch
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from collections import Counter
import pandas as pd
import numpy as np
import string

# embeddings for each genre
comedy_2d = torch.load("comedy_embeddings.pt")
tragedy_2d = torch.load("tragedy_embeddings.pt")
history_2d = torch.load("history_embeddings.pt")

# a numpy array storing common words between the plays
common_words = np.load("common_words.npy")
common_words = common_words[1:]
# a numpy array containing all unique words in plays
all_words = np.load("all_words.npy")
# a dict storing index for each word
common_dict = {all_words[i]:i for i in range(len(all_words))}



#banned words because they are not very interesting to look at
banned_words = ['well', 'so', 'what', 'hence', 'there', 'on', 'indeed', 'you', 'do', 'this',
                'thus', 'here', 'him', 'say', 'thee', 'be', 'it','thou', 'to', 'come', 'go', 'away',
                'he', 'more', 'one', 'see', 'speak', 'stay', 'that', 'then', 'up', 'yet', 'by', 'all',
                'in', 'we', 'again', 'down', 'enough', 'for', 'have', 'her', 'himself', 'hold', 'how',
                'no', 'i', 'now', 'me', 'mine', 'none', 'not', 'of', 'still', 'out', 'farewell', 'fellow'
                'words', 'right', 'time', 'done', 'gentlemen', 'grace', 'sir', 'fellow', 'help', 'lady', 
                'myself', 'long', 'masters', 'name', 'queen', 'rest', 'sons', 'stand', 'tomorrow', 'tonight', 'words'
                'together', 'too', 'will', 'a', 'o', 'am', 'another', 'answer', 'are', 'arm', 'bear', 'best', 'both'
                'cause', 'comes', 'arms', 'art', 'back', 'both', 'cause', 'cousin', 'daughter', 'ever', 'fall',
                'first', 'fly', 'further', 'his', 'pardon', 'much', 'madam', 'look', 'leave', 'last', 'leave',
                'look', 'madam', 'much', 'pardon', 'sleep', 'she', 'shall', 'ill', 'is', 'know', 'upon', 'thyself',
                'think', 'thine', 'thanks', 'tell', 'sister', 'return', 'prince', 'aside', 'wife', 'welcome',
                'eye']
mask_ban = ~np.isin(common_words, banned_words)

# another option to limit word count
preferred_word = ['lord', 'good', 'dead', 'love', 'true', 'faith', 'death', 'honour', 
                  'god', 'die', 'hell', 'heaven', 'joy', 'patience', 'nothing', 'shame',
                  'fear', 'fortune', 'enemies']
mask_inc = np.isin(common_words, preferred_word)


common_words = common_words[mask_ban]
# limiting max words becaues there are too many words to look at
max_words = 50
common_words = common_words[:max_words]


#used to help with graphing
comedy_points = np.array([comedy_2d[common_dict[i]] for i in common_words])
comedy_data = pd.DataFrame({
    'x':comedy_points[:, 0],
    'y':comedy_points[:, 1],
    'genre':'comedy',
    'word':common_words
})

tragedy_points = np.array([tragedy_2d[common_dict[i]] for i in common_words])
tragedy_data = pd.DataFrame({
    'x':tragedy_points[:, 0],
    'y':tragedy_points[:, 1],
    'genre':'tragedy',
    'word':common_words
})

history_points = np.array([history_2d[common_dict[i]] for i in common_words])
history_data = pd.DataFrame({
    'x':history_points[:, 0],
    'y':history_points[:, 1],
    'genre':'history',
    'word':common_words
})



app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id="scatter-plot"),
    html.P("percentage of words shown"),
    dcc.Slider(
        id='slider',
        min=10, max=100, step=10,
        value=10),
    html.P("Select genres:"),
    dcc.Checklist(
        id='checklist',
        options=[
            {'label': 'Comedy', 'value': 'comedy'},
            {'label': 'Tragedy', 'value': 'tragedy'},
            {'label': 'History', 'value': 'history'}
        ],
        value=['comedy', 'tragedy', 'history'],  
    ),
])

@app.callback(
    Output("scatter-plot", "figure"), 
    Input("slider", "value"),
    Input("checklist", "value"))

def update_plot(percentage, genres):
    global comedy_data, tragedy_data, history_data
    if genres == []:
        return px.scatter()
    max = int(comedy_data.shape[0] * percentage/100)
    lim_comedy_data = comedy_data[:max]
    lim_tragedy_data = tragedy_data[:max]
    lim_history_data = history_data[:max]

    data = pd.DataFrame({
        'x':[0,0,0],
        'y':[-100,-100,-100],
        'genre':['comedy', 'tragedy', 'history'],
    })
    if 'comedy' in genres:
        data = pd.concat([data,lim_comedy_data])
    if 'tragedy' in genres:
        data = pd.concat([data,lim_tragedy_data])
    if 'history' in genres:
        data = pd.concat([data,lim_history_data])
    fig = px.scatter(data, x="x", y="y", color="word", symbol='genre', hover_name='word')
    fig.update_yaxes(range = [-5,5])
    fig.update_xaxes(range = [-5,5])
    return fig

app.run_server(debug=True)


