import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

# Define app
app = dash.Dash()

# Define the layout of the app
app.layout = html.Div(children = [
    dcc.Input(id='input', value='Enter a string here!', type='text'),
    html.Div(id='output')
])

# Define a wrapper for the input/output of the user data
@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='input', component_property='value')]
)

# Define the functio to retrun the input of the user as the output
def input_value(input_date):
    return 'Input: "{}"'.format(input_date)

# Run the server
if __name__ == '__main__':
    app.run_server(debug = True)
