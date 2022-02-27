# coding: utf-8

from dash import html, dcc, callback, callback_context
from dash.dependencies import Input, Output, State
import dash_latex as dl
import dash_daq as daq
from matplotlib.pyplot import show

import numpy as np
from . import atomic_orbitals as ao
#from .ao_angular import angular_part_equations, angular_part_data, get_polar_plot

""" This module implements the components for the angular probability density tab """

__author__ = "Germain Salvato Vallverdu"
__email__ = "germain.vallverdu@univ-pau.fr"


# Documentation of this tab
# --------------------------
text_doc = [
    html.H3("Theory: Atomic orbitals"),
    html.P("""Atomic orbitals are monoelectronic wavefunctions, 
        solutions of the Schrödinger equation of an Hydrogenoid system
        with an atomic number Z. The 
        general expression of the atomic orbital reads"""),
    dl.DashLatex(r"""
    $$
        \phi_{n,\ell,m_{\ell}}\left(r,\theta,\varphi\right) = 
            R_{n,\ell}(r) \, Y_{\ell}^{m_{\ell}}(\theta, \varphi)
    $$
    """, displayMode=True),
    html.P("""The above figure displays a view of the electronic cloud
    associated to the selected atomic orbital. Each point represents the 
    position of the electron assuming we are able to take an instantaneous 
    picture of the system and record the position of the electron."""),
]


def atomic_orbital_tab():
    return dcc.Tab(
        label=" Atomic orbitals cloud", className="fas fa-cloud custom-tab",
        value="atomic-orbitals",
        selected_className='custom-tab--selected',
        children=[
            html.Div(className="custom-tab-container", children=[
                dcc.Store(id="atomic-orbital-data"),
                html.H3("Atomic orbitals - Overview of the electronic cloud"),
                html.Div([
                    html.Div([
                        html.H4("Atomic orbital:", style={
                                "padding-left": "10px"}),
                        dcc.Dropdown(
                            options=[k for k in ao.ao_data],
                            id="atomic-orbital-dropdown",
                            placeholder="Select an atomic orbital",
                            value="1s",
                        ),
                    ]),
                    html.Div([
                        html.H4("Number of points", style={
                                "padding-left": "10px"}),
                        dcc.Slider(
                            id="ao-npts-slider",
                            min=1, max=1000, step=1, value=250,
                            marks={i: {"label": str(i)}
                                   for i in range(0, 1000, 100)},
                            tooltip=dict(placement="bottom",
                                         always_visible=True)
                        ),
                    ]),
                    html.Div([
                        html.H4("Sign", style={"padding-left": "10px"}),
                        html.Div([
                            daq.BooleanSwitch(id="ao-show-sign", on=False),
                            html.P(id="ao-show-sign-text"),
                        ],
                            style={"display": "grid",
                                   "grid-template-columns": "40% 60%"}
                        ),
                    ]),
                    html.Div([
                        html.H4("Nodal planes", style={
                                "padding-left": "10px"}),
                        html.Div([
                            daq.BooleanSwitch(id="ao-show-nodal", on=True),
                            html.P(id="ao-show-nodal-text"),
                        ],
                            style={"display": "grid",
                                   "grid-template-columns": "40% 60%"}
                        ),
                    ]),
                    html.Div([
                        html.H4("Replot", style={"padding-left": "10px"}),
                        html.Button("run", id="ao-replot-btn", n_clicks=0),
                    ]),
                ],
                    style={
                        "display": "grid",
                        "grid-template-columns": "20% 35% 15% 15% 15%"}
                ),

                # plot
                dcc.Graph(id="atomic-orbital-graph"),

                # docs
                html.Div(className="docs", children=text_doc),
            ])
        ])


@callback(
    [Output("atomic-orbital-graph", 'figure'),
     Output("ao-show-sign-text", "children"),
     Output("ao-show-nodal-text", "children"),
     Output("atomic-orbital-data", "data")],
    [Input("atomic-orbital-dropdown", "value"),
     Input("ao-npts-slider", "value"),
     Input("ao-replot-btn", "n_clicks"),
     Input("ao-show-sign", "on"),
     Input("ao-show-nodal", "on")],
    State("atomic-orbital-data", "data")
)
def display_graph(ao_name, npts, n_clicks_replot, show_sign, show_nodal, data):
    """ This function produce the polar plot from the dropdown selection """

    ctx = callback_context
    sign_text = "On" if show_sign else "Off"
    nodal_text = "On" if show_nodal else "Off"

    if (ctx.triggered[0]["prop_id"] == "ao-show-sign.on" or
            ctx.triggered[0]["prop_id"] == "ao-show-nodal.on"):
        points = np.array(data["points"])
        wf = np.array(data["wf"])
        fig = ao.get_plot(ao_name, ntry=npts, points=points, wf=wf,
                          show_sign=show_sign, show_nodal=show_nodal)

    else:
        ao_function = ao.ao_data[ao_name]["function"]
        rmax = ao.ao_data[ao_name]["rmax"]
        points, wf = ao.sample(ao_function, rmax=rmax, ntry=npts)
        data = dict(points=points, wf=wf)
        fig = ao.get_plot(ao_name, points=points, ntry=npts, wf=wf,
                          show_sign=show_sign, show_nodal=show_nodal)

    return fig, sign_text, nodal_text, data
