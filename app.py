#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html

from components import header, footer
from components import (particle_box_components, ao_radial_components,
                        ao_angular_components, ao_components)

# Set up app
# ------------------------------------------------------------------------------
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    "https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
]

TITLE = "Wavefunctions and atomic orbitals in Quantum Chemistry"
URL = "https://github.com/gVallverdu/probability-density-qm"

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = TITLE

app.layout = html.Div(className="container", children=[
    header(TITLE, URL, fa_icon="fas fa-atom"),

    html.Div([
        dcc.Tabs([
            particle_box_components.particle_box_tab(),
            ao_radial_components.radial_part_tab(),
            ao_angular_components.angular_part_tab(),
            ao_components.atomic_orbital_tab(),
        ],
            value="particle-in-a-box",
            # value="AO-radial-part",
            # value="AO-angular-part",
            # value="atomic-orbitals",
        ),
    ]),

    footer(
        logo_img="http://gvallver.perso.univ-pau.fr/img/logo_uppa.png",
        logo_url="https://www.univ-pau.fr"
    ),
])

if __name__ == '__main__':
    # app.run_server(debug=True, host='127.0.0.1')
    app.run_server(debug=False)
