# coding: utf-8

from dash import html, dcc, callback, callback_context
from dash.dependencies import Input, Output, State
import dash_latex as dl
import plotly.graph_objects as go

import numpy as np
from .atomic_orbitals import AORadialPart, radial_part_equations

""" This module implements the components for radial probability density tab """

__author__ = "Germain Salvato Vallverdu"
__email__ = "germain.vallverdu@univ-pau.fr"

# parameter
NPTS_MAX = 1000

# Documentation of this tab
# --------------------------
text_doc = [
    html.H3("Theory: Radial part of atomic orbitals"),
    html.P("""Atomic orbitals are monoelectronic wavefunctions, 
        solutions of the Schrödinger equation for the hydrogen atom. The 
        general expression of the atomic orbital reads"""),
    dl.DashLatex(r"""
    $$
        \phi_{n,\ell,m_{\ell}}\left(r,\theta,\varphi\right) = 
            R_{n,\ell}(r) \, Y_{\ell}^{m_{\ell}}(\theta, \varphi)
    $$
    """, displayMode=True),
    html.P("""The radial part controls the expension of the atomic
    orbital. The general expression of the radial part reads"""),
    dl.DashLatex(r"""
    $$
        R_{n, \ell}(r) = P_{n,\ell}(r) \exp\left(-\frac{Zr}{n a_o}\right)
    $$
    """, displayMode=True),
    html.P("Hereafter, the equations of the radial parts for the lowest quantum numbers:"),
    dl.DashLatex(radial_part_equations, displayMode=True),
]


def selector(val_max, title, base_id, value=1, step=1, step_slider=5, val_min=1):
    return html.Div([
        html.H4(title),
        html.Div([
            html.Button(
                html.Span(className="fas fa-minus-square fa-3x"),
                id=f"{base_id}-minus-btn", n_clicks=0, className="pm-btn",
                style={"textAlign": "right"}
            ),
            dcc.Slider(
                id=f"{base_id}-slider",
                min=val_min, max=val_max, step=step, value=value,
                marks={i: {"label": str(i)}
                       for i in range(0, val_max + step_slider, step_slider)},
                tooltip=dict(placement="bottom",
                             always_visible=True)
            ),
            html.Button(
                html.Span(className="fas fa-plus-square fa-3x"),
                id=f"{base_id}-plus-btn", n_clicks=0, className="pm-btn",
                style={"textAlign": "left"}
            )],
            style={"display": "grid",
                   "grid-template-columns": "15% 70% 15%"}
        ),
    ])


def radial_part_tab():
    return dcc.Tab(
        label=" AO Radial part", className="fas fa-chart-area custom-tab",
        selected_className='custom-tab--selected',
        children=[
            html.Div(className="custom-tab-container", children=[
                html.H3("Atomic orbitals - Radial probability density"),
                html.Div(children=[
                    # select n value
                    selector(val_max=AORadialPart.n_max, base_id="n-radial",
                             value=1, step=1, step_slider=1,
                             title="Value of the principal quantum number n",),
                    # select n value
                    selector(val_max=AORadialPart.n_max - 1, base_id="l-radial",
                             value=0, val_min=0, step=1, step_slider=1,
                             title="Value of the secondary quantum number l",),
                ],
                    style={"display": "grid",
                           "grid-template-columns": "35% 35% 20% 10%"}
                ),

                # plot
                html.Div(
                    dcc.Graph(id="radial-density-graph"),
                ),

                html.Div(className="docs", children=text_doc),
            ])
        ])


@callback(
    Output("n-radial-slider", "value"),
    [Input("n-radial-plus-btn", "n_clicks"),
     Input("n-radial-minus-btn", "n_clicks")],
    State("n-radial-slider", "value"),
)
def increase_n(click_plus, click_minus, n):
    ctx = callback_context

    if ctx.triggered[0]["prop_id"] == "n-radial-plus-btn.n_clicks":
        if n < AORadialPart.n_max:
            return n + 1
        else:
            return n

    elif ctx.triggered[0]["prop_id"] == "n-radial-minus-btn.n_clicks":
        if n > 1:
            return n - 1
        else:
            return n

    else:
        return n


@callback(
    Output("l-radial-slider", "value"),
    [Input("l-radial-plus-btn", "n_clicks"),
     Input("l-radial-minus-btn", "n_clicks"),
     Input("n-radial-slider", "value")],
    State("l-radial-slider", "value"),
)
def increase_l(click_plus, click_minus, n, l):
    ctx = callback_context

    if ctx.triggered[0]["prop_id"] == "l-radial-plus-btn.n_clicks":
        if l < n - 1:
            return l + 1
        else:
            return l

    elif ctx.triggered[0]["prop_id"] == "l-radial-minus-btn.n_clicks":
        if l > 0:
            return l - 1
        else:
            return l

    else:
        return l


@callback(
    Output("radial-density-graph", 'figure'),
    [Input("n-radial-slider", "value"),
     Input("l-radial-slider", "value")],
)
def display_graph(n, l):
    """ This function produce the plot from the sliders or the replot
    button. """

    radial_part = AORadialPart(n, l)

    return radial_part.get_plot()
