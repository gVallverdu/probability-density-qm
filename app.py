#!/usr/bin/env python
# coding: utf-8

import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import pandas as pd

# read data file
# ------------------------------------------------------------------------------
df = pd.read_csv(
    "nba_physiques.csv",
    index_col=0,
    dtype={"Year": "int"}
)
# manage data
df = df.assign(bmi=df.weight / ((df.height / 100) ** 2))
df = df.assign(ht_bins=pd.qcut(df.height, q=4))
df = df[["Year", "height", "weight", "bmi",
         "PER", "PTS", "pos_simple", "ht_bins"]]


# Set up app
# ------------------------------------------------------------------------------
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# HTML page Layout
# ------------------------------------------------------------------------------
# Page is divided in three parts:
#    * header: at the top, a title
#    * body: the main containt
#    * footer: at the bottom, contact, informations, credits
app.layout = html.Div(className="", children=[
    # ------ header
    html.Div(
        className="header",
        style={"backgroundColor": "#3c6382"},
        children=[html.H2(
            "Stats on NBA players - Dash app example",
            style={
                "color": "white",
                "padding": "30px 0 30px 0",
                "textAlign": "center"}
        )],
    ),

    # ----- body
    html.Div(className="body", children=[
        # a sub title
        html.H3("A plot"),
        # first dropdown selector
        dcc.Dropdown(
            id="x-dropdown",  # identifiant
            value="height",  # default value
            # all values in the menu
            options=[{"label": name, "value": name} for name in df.columns],
        ),
        # second dropdown selector
        dcc.Dropdown(
            id="y-dropdown",
            value="weight",
            options=[{"label": name, "value": name} for name in df.columns],
        ),
        # a place for the plot with an id
        html.Div(
            dcc.Graph(id='graph'),
        ),
        # a line
        html.Hr(),
        # a sub title
        html.H3("A table"),
        # a new dropdown
        dcc.Dropdown(
            id="pivot-dropdown",
            value="height",
            options=[{"label": name, "value": name} for name in df.columns],
        ),
        # a table for data
        dash_table.DataTable(
            id="pivot-table",
        ),
        html.Div(id="table")
    ]),

    # ----- footer
    html.Div(
        className="footer",
        style={"backgroundColor": "#3c6382"},
        children=[html.H2(
            "https://github.com/gVallverdu/dash-example-NBA",
            style={
                "color": "white",
                "padding": "30px 0 30px 0",
                "textAlign": "center"}
        )],
    ),
])

# Callback functions => interactivity
# Each element on the page is identified thanks to its `id`
# ------------------------------------------------------------------------------


@app.callback(
    Output('graph', 'figure'),
    [Input("x-dropdown", "value"),
     Input("y-dropdown", "value")],
)
def display_graph(xvalue, yvalue):
    """ 
    This function produce the plot.

    The output is the "figure" of the graph
    The inputs, are the values of the two dropdown menus
    """

    figure = px.scatter(
        df,
        x=xvalue, y=yvalue,
        color='pos_simple',
        category_orders=dict(pos_simple=['PG', 'SG', 'SF', 'PF', 'C']),
        marginal_x="histogram",
        marginal_y="histogram",
        animation_group="Year",
        template="plotly_white",
    )

    return figure


@app.callback(
    [Output("pivot-table", "data"),
     Output("pivot-table", "columns")],
    [Input("pivot-dropdown", "value")]
)
def show_pivot_table(value):
    """ This function return a pivot Table """

    pivot_df = pd.pivot_table(
        data=df, values=value, columns="pos_simple", index="ht_bins"
    )
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.astype({"ht_bins": "str"})
    cols = [{"name": col, "id": col} for col in pivot_df.columns]
    data = pivot_df.to_dict("records")

    return data, cols


if __name__ == '__main__':
    app.run_server(debug=True)
