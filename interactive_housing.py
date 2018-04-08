import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pandas_datareader as web
from dash.dependencies import Input, Output
import datetime

# Define app
app = dash.Dash()

# Gathering data
# TODO: Change from stock price information to housing markets
stock = 'TSLA'
start = datetime.datetime(2015, 1, 1)
end = datetime.datetime(2018, 2, 8)
df = web.DataReader(stock, 'morningstar', start, end)
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)
df = df.drop("Symbol", axis=1)

# Set the layout of the graph
app.layout = html.Div(children = [

    # Main Title
    html.H1(children = 'Housing Price Viewer'),

    # Sub Title
    html.Div(children = '''
                        This is a quick little app thrown together to view housing prices
                        over a number of housing markets throughout the country.
                        '''),

    # Define the graph layout
    dcc.Graph(
    id = 'graph',
    figure={
        'data': [
            {'x': df.index, 'y': df.Close, 'type': 'line', 'name': stock},
        ],
                'layout': {
                    'title': stock
                }
        }
    )

])

# Run the server
if __name__ == '__main__':
    app.run_server(debug = True)
