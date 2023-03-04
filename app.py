import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_table
from dash.dependencies import Input, Output, State

# Load the data
df = pd.read_csv('data.csv')

# Define the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.Header([
        html.Img(src="/asset/logo.png", alt="Logo", style={"float": "left", "height": "100px", "display":"block"}),
        html.Img(src="uni.jpg", alt="University", style={"display": "block", "margin": "auto", "height": "100px"}),
        html.Nav(style={"text-align": "center"}, children=[
            html.Ul(style={"display": "inline-block"}, children=[
                html.Li(style={"display": "inline-block", "margin-right": "300px"}, children=[
                    html.A("Home", href="home.html", style={"font-size": "30px", "font-weight": "bold", "text-decoration": "none", "color": "black"})
                ]),
                html.Li(style={"display": "inline-block", "margin-right": "300px"}, children=[
                    html.A("Analysis", href="analysis.html", style={"font-size": "30px", "font-weight": "bold", "text-decoration": "none", "color": "black"})
                ]),
                html.Li(style={"display": "inline-block"}, children=[
                    html.A("Contact Us", href="contact.html", style={"font-size": "30px", "font-weight": "bold", "text-decoration": "none", "color": "black"})
                ])
            ])
        ])
    ]),
    html.Main([
        html.H1("Network Graph"),
        html.Div([
            dcc.Input(id='search-box', type='text', placeholder='Enter a node', style={'width': '40%'}),
            html.Button('Submit', id='submit-button', style={'marginLeft': '10px'})
        ], style={'display': 'flex', 'justifyContent': 'center'}),
        html.Br(),
        cyto.Cytoscape(
            id='cytoscape',
            elements=[],
            layout={'name': 'cose'},
            style={'width': '60%', 'height': '500px', 'margin': 'auto'}
        ),
        html.Br(),
        html.H3("Searching Node Information"),
        dash_table.DataTable(
            id='search-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'center',
                'minWidth': '0px', 'maxWidth': '180px',
                'whiteSpace': 'normal',
                'textOverflow': 'ellipsis',
                'fontSize': '12pt'
            }
        ),
        html.H3("Interconnecting Nodes Information"),
        dash_table.DataTable(
            id='interconnecting-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'center',
                'minWidth': '0px', 'maxWidth': '180px',
                'whiteSpace': 'normal',
                'textOverflow': 'ellipsis',
                'fontSize': '12pt'
            }
        )
    ])
])

# Define the callback
@app.callback(
    [Output('cytoscape', 'elements'),
     Output('search-table', 'data'),
     Output('interconnecting-table', 'data')],
    Input('submit-button', 'n_clicks'),
    State('search-box', 'value')
)
def update_graph(n_clicks, search_term):
    if not search_term:
        return [], [], []
    # Filter the dataframe to only show the interconnections of the search term
    sub_df = df[(df['node_a'] == search_term) | (df['node_b'] == search_term)]
    # Convert the dataframe to a list of cytoscape elements
    elements = [{'data': {'id': node, 'label': node}} for node in pd.unique(sub_df[['node_a', 'node_b']].values.ravel('K'))]
    edges = [{'data': {'source': row['node_a'], 'target': row['node_b']}} for index, row in sub_df.iterrows()]
    elements.extend(edges)
    # Return the updated graph and the table data
    return elements, [sub_df[sub_df['node_a'] == search_term].iloc[0].to_dict()], sub_df.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
