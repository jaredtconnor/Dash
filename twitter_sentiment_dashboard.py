import sqlite3 as sql
import pandas as pd
import dash
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html

conn = sql.connect("twitter_sentiment.db")
cursor = conn.cursor()

def create_table():
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
        cursor.execute("CREATE INDEX fast_unix ON sentiment(unix)")
        cursor.execute("CREATE INDEX fast_tweet ON sentiment(tweet)")
        cursor.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
        conn.commit()
    except Exception as e:
        print(str(e))

create_table()

ckey="JfhNSUpRBnCkQekjkTOIL86uR"
csecret="StOVv2LE3HASVAp1pPP3sZkbucEXnPLMssVAcxPsQ3F7POAaxA"
atoken="444822244-BnyUlvHCrRJ0gB7LLgZOuH96aSfMrL9f8Mi8mXRT"
asecret="EWpuLcNJ3WcNCmBQ17b1CBwPtAviBQyb0jgI9KGdZvsiU"

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H2("Live Twitter Sentiment"),
        dcc.Graph(id = 'live-graph', animate = True),
        dcc.Interval(
            id = 'graph-update',
            interval = 1*1000
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
              events = [Event('graph-update', 'interval')])

def updated_graph_scatter():
    try:
        conn = sql.connect("twitter_sentiment.db")
        cursor = conn.cursor()
        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKFE %royal% ORDER BY unix DESC LIMIT 1000", con = conn)
        df.sort_values('unix', inplace = True)
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/5)).mean()
        df.dropna(inplace=True)

        X = df.unix.values[-100:]
        Y = df.sentiment_smoothed.values[-100:]

        data = plotly.graph_objs.Scatter(
            x = list(X),
            y = list(Y),
            name = 'Scatter',
            mode = 'lines+markers'
        )

        return {'data': [data], 'layout': go.Layout(xaxis = dict(range=[min(X),max(X)]),
                                                    yaxis = dict(range=[min(Y),max(Y)]),)}

    except Exception as e:
        with open('errors.txt', 'a') as error:
            error.write(str(e))
            error.write("\n")

if __name__ == '__main__':
    app.run_server(debug = True)
