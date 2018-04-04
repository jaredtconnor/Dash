import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children = [
    html.H1(children = "Hello Dash"),


    html.Div(children = '''
    Dash: A web application framework for Python and graphing awesome things!
    '''),

    dcc.Graph(
        id = 'Graph Example',
        figure = {
            'data': [
                {'x': [1,2,3], 'y': [4,6,1], 'type': 'bar', 'name': 'Oregon'},
                {'x': [1,2,3], 'y': [1,2,4], 'type': 'bar', 'name': 'California'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }

    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
