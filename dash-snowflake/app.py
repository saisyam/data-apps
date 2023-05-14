from snowflake.snowpark import Session
from dotenv import load_dotenv
import os
from dash import Dash, html, Input, Output, dcc, callback, dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_dotenv()

load_figure_template("cerulean")
connection_params = {
    "account": os.getenv("ACCOUNT"),
    "user": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD"),
    "database": os.getenv("DATABASE"),
    "schema": os.getenv("SCHEMA"),
    "role": os.getenv("ROLE")
}

session = Session.builder.configs(connection_params).create()
df = session.sql("select * from reviews").to_pandas()

# Initialize the app
# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN, dbc_css])

header = html.H4(
    "Data Apps with Dash and Snowflake", className="bg-primary text-white p-2 mb-2 text-center"
)
restaurants = df['RESTAURANT'].unique()

dropdown = html.Div(
    [
        dbc.Label("Select Restaurant"),
        dcc.Dropdown(
            restaurants,
            "Taco Bell",
            id="restaurant",
            clearable=False,
        ),
    ],
    className="mb-4",
)
bar_graph = html.Div(
    [
        dcc.Graph(figure={}, id="reviews-bar-chart")
    ]
)
controls = dbc.Card(
    [dropdown, bar_graph],
    body=True,
)

app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [
                dbc.Col(
                    [
                        controls,
                    ],
                    width=4,
                ),
                #dbc.Col([tabs, colors], width=8),
            ]
        ),
    ],
    fluid=True,
    className="dbc",
)

@callback(
    Output("reviews-bar-chart", "figure"),
    Input("restaurant", "value"),
)
def update_bar_chart(restaurant):
    df3 = df.query("RESTAURANT == '"+restaurant+"'").groupby(['RATING'])["RATING"].count().reset_index(name="COUNT")
    fig = px.bar(
        df3,
        x="COUNT",
        y="RATING",
        title="Reviews count by rating",
        orientation='h'
    )
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)