#!/usr/bin/env python
# coding: utf-8

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html

from components import header, footer
from components import particle_box_components as pbc
from components import ao_radial_components

# Set up app
# ------------------------------------------------------------------------------
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
]

TITLE = "Probability density - Quantum chemistry"
URL = "https://github.com/gVallverdu/probability-density-qm"

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = TITLE

app.layout = html.Div(className="container", children=[
    header(TITLE, URL, fa_icon="fas fa-atom"),

    html.Div([
        dcc.Tabs([
            pbc.particle_box_tab(),
            ao_radial_components.radial_part_tab(),
        ]),
    ]),

    footer(
        logo_img="http://gvallver.perso.univ-pau.fr/img/logo_uppa.png",
        logo_url="https://www.univ-pau.fr"
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
