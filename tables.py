import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv(
    '/Users/Jared/Documents/Programming/Python/Data_Analysis/Dash/datasets/A191RL1Q225SBEA.csv'
)


def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )



# Init the server
app = dash.Dash()

# Define the layout
app.layout = html.Div(children = [
    html.H4(children = 'US GDP Data'),
    html.P(children = "Quaterly data - 1947 - 2018",
           style = {
           'textAlign': 'center'
           }),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug = True)
