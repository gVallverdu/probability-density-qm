#!/usr/bin/env python
# coding: utf-8

import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash_table.Format import Format

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
df = df.assign(height_bins=pd.qcut(df.height, q=4))
df = df[["Year", "height", "weight", "bmi",
         "PER", "PTS", "pos_simple", "height_bins"]]


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
app.layout = html.Div(className="container", children=[
    dcc.Dropdown(
        id="pivot-dropdown",
        value="height",
        options=[
            {"label": name, "value": name} 
            for name in ["Year", "height", "weight", "bmi", "PER", "PTS"]
        ],
    ),
    # a table for data
    dash_table.DataTable(
        id="pivot-table",
    ),
])

# Callback functions => interactivity
# Each element on the page is identified thanks to its `id`
# ------------------------------------------------------------------------------


@app.callback(
    [Output("pivot-table", "data"),
     Output("pivot-table", "columns")],
    [Input("pivot-dropdown", "value")]
)
def show_pivot_table(value):
    """ This function return a pivot Table """

    pivot_df = pd.pivot_table(
        data=df, values=value, columns="pos_simple", index="height_bins"
    )
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.astype({"height_bins": "str"})
    cols = [{
        "name": col, 
        "id": col, 
        "type": "numeric",
        "format": Format(precision=5)
        } for col in pivot_df.columns]
    data = pivot_df.to_dict("records")

    return data, cols


if __name__ == '__main__':
    app.run_server(debug=True)
