import sqlite3 as sql
import pandas as pd
import dash
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from dash.dependencies import Output, Event, Input
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.H2("Live Twitter Sentiment"),
        dcc.Input(id = "sentiment_keyword", value = 'twitter', type = 'text'),
        dcc.Graph(id = 'live-graph', animate = True),
        dcc.Interval(
            id = 'graph-update',
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
              [Input(component_id = 'sentiment_keyword', component_property = 'value')],
              events = [Event('graph-update', 'interval')])

def updated_graph_scatter():
    try:
        conn = sql.connect("twitter_sentiment.db")
        cursor = conn.cursor()
        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000", conn, params = ('%' + sentiment_keyword + '%',))
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
                                                    yaxis = dict(range=[min(Y),max(Y)]),
                                                    title = f"Term: {sentiment_keyword}")
                                                    }


    except Exception as e:
        with open('errors.txt', 'a') as error:
            error.write(str(e))
            error.write("\n")

if __name__ == '__main__':
    app.run_server(debug = True)
