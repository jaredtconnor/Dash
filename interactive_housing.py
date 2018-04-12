import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

stock = 'TSLA'
start = datetime.datetime(2015,1,1)
end = datetime.datetime.now()
df = web.DataReader(stock, 'morningstar', start, end)
df.reset_index(inplace=True)
df = df.drop("Symbol", axis = 1)

app.layout = html.Div(children = [

    html.H1(children = 'Housing Price Graph'),

    html.Div(children = '''

    Making a stock graph!

    '''),

    dcc.Graph(

        id = 'graph',
        figure = {
            'data': [
            {'x': df.index, 'y': df.Close, 'type': 'line', 'name': stock},
        ],
        'layout': {
            'title': stock
            }
        }
      )
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
