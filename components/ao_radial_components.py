# coding: utf-8

from dash import html, dcc, callback, callback_context
from dash.dependencies import Input, Output, State
import dash_latex as dl
import plotly.graph_objects as go

import numpy as np
from .ao_radial import AORadialPart, radial_part_equations

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
        solutions of the Schrödinger equation of an Hydrogenoid system
        with an atomic number Z. The 
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
    html.P("Hereafter, are displayed the equations of the radial parts of"
           " the atomic orbitals for the lowest quantum numbers:"),
    dl.DashLatex(radial_part_equations, displayMode=True),
    dl.DashLatex("The radial probability density is ususally named "
                 " $\mathcal{D}(r)$ and reads:"),
    dl.DashLatex(r"""
    $$
        \mathcal{D}(r) = r^2 \vert R_{n,\ell}(r)\vert^2
    $$""", displayMode=True),
    dl.DashLatex(r"""Using the radial probability density, the probability
    to find an electron between two spheres of radius $r_1$ and $r_2$ is
    is given by:"""),
    dl.DashLatex(r"""
        $$
        P(e^-\in[r_1;r_2]) = \int_{r_1}^{r_2} r^2 \vert R_{n,\ell}(r)\vert^2 dr
        $$""", displayMode=True),
]


def nl_selector(title, base_id, value=1, val_min=0, val_max=4):
    return html.Div([
        dcc.ConfirmDialog(id=f"{base_id}-error-dialog"),
        html.Div([
            html.Div(
                [dl.DashLatex(title)],
                style={"textAlign": "right", "fontSize": "large"}
            ),
            html.P(f"{value}", id=f"{base_id}-number",
                   style={"textAlign": "left", "fontSize": "large"}),
            html.Button(
                html.Span(className="fas fa-minus-square fa-3x"),
                id=f"{base_id}-minus-btn", n_clicks=0, className="pm-btn",
            ),
            html.Button(
                html.Span(className="fas fa-plus-square fa-3x"),
                id=f"{base_id}-plus-btn", n_clicks=0, className="pm-btn",
            ),
        ],
            style={"display": "grid",
                   "grid-template-columns": "30% 30% 20% 20%"}
        )
    ])


def radial_part_tab():
    return dcc.Tab(
        label=" Radial part of AO", className="fas fa-chart-area custom-tab",
        value="AO-radial-part",
        selected_className='custom-tab--selected',
        children=[
            html.Div(className="custom-tab-container", children=[
                html.H3("Atomic orbitals - Radial probability density"),
                html.Div([
                    html.Div([
                        html.H4("Select quantum numbers"),
                        html.Div([
                            # select n value
                            nl_selector(base_id="n-radial", title=r"$n=\;$ "),
                            # select l value
                            nl_selector(base_id="l-radial",
                                        title=r"$\ell=\;$ ", value=0),
                        ],
                            style={"display": "grid",
                                   "padding": "0 20px",
                                   "grid-template-columns": "50% 50%"}
                        ),

                        # plot
                        dcc.Graph(id="radial-density-graph"),
                    ]),
                    html.Div(className="docs", children=[
                        html.H4("Integrate the radial proability density"),
                        dl.DashLatex(r"In order to compute the probability $P(V)$"
                                     " to find an electron between two spheres of radius"
                                     " $r_1$ and $r_2$, one has to compute the integral"
                                     " of the radial probability density such as:"),
                        dl.DashLatex(r"""
                            $$
                            P(e^-\in[r_1;r_2]) = \int_{r_1}^{r_2} r^2 \vert R_{n,\ell}(r)\vert^2 dr
                            $$
                        """, displayMode=True),
                        dl.DashLatex(r"Fill in the values of the integration"
                                     r" boundaries $r_1$ and $r_2$ in $\text{\AA}$ and click on"
                                     " compute."),
                        html.Div([
                            dcc.Input(
                                id="radial-integrate-minval", type="number", step=.1,
                                placeholder="r_1", debounce=True, min=0, max=15,
                            ),
                            dcc.Input(
                                id="radial-integrate-maxval", type="number",  # step=.1,
                                placeholder="r_2", debounce=True, min=0, max=30,
                            ),
                            html.Button(
                                [html.Span(
                                    className="fas fa-calculator"), " Compute"],
                                id="run-integration-btn", n_clicks=0,
                            )
                        ],
                            style={"display": "grid", "margin": "20px 0",
                                   "grid-template-columns": "35% 35% 30%"}
                        ),
                        html.Div(id="radial-integration-result")
                    ],
                        style={
                            "border-left": "1px solid LightGray",
                            "padding-left": "10px",
                    }
                    ),
                ],
                    style={"display": "grid",
                           "grid-template-columns": "50% 50%"}
                ),

                # docs
                html.Div(className="docs", children=text_doc),
            ])
        ])


@callback(
    [Output("n-radial-number", "children"),
     Output("n-radial-error-dialog", "displayed"),
     Output("n-radial-error-dialog", "message")],
    [Input("n-radial-plus-btn", "n_clicks"),
     Input("n-radial-minus-btn", "n_clicks")],
    State("n-radial-number", "children"),
)
def increase_n(click_plus, click_minus, n_str):
    ctx = callback_context
    n = int(n_str)

    n_return = n_str
    show_message = False
    message = ""

    if ctx.triggered[0]["prop_id"] == "n-radial-plus-btn.n_clicks":
        if n < AORadialPart.n_max:
            n_return = f"{n + 1}"
        else:
            show_message = True
            message = f"Maxmum value of n is {AORadialPart.n_max}."

    elif ctx.triggered[0]["prop_id"] == "n-radial-minus-btn.n_clicks":
        if n > 1:
            n_return = f"{n - 1}"
        else:
            show_message = True
            message = f"Minimum value of n is 1"

    return n_return, show_message, message


@callback(
    Output("l-radial-number", "children"),
    [Input("l-radial-plus-btn", "n_clicks"),
     Input("l-radial-minus-btn", "n_clicks"),
     Input("n-radial-number", "children")],
    State("l-radial-number", "children"),
)
def increase_l(click_plus, click_minus, n_str, l_str):
    ctx = callback_context
    l = int(l_str)
    n = int(n_str)

    if ctx.triggered[0]["prop_id"] == "l-radial-plus-btn.n_clicks":
        if l < n - 1:
            return f"{l + 1}"
        else:
            return l_str
            # return dcc.ConfirmDialog("Error value l!")

    elif ctx.triggered[0]["prop_id"] == "l-radial-minus-btn.n_clicks":
        if l > 0:
            return f"{l - 1}"
        else:
            return l_str

    else:
        return l_str


@callback(
    [Output("radial-density-graph", 'figure'),
     Output("radial-integration-result", "children")],
    [Input("n-radial-number", "children"),
     Input("l-radial-number", "children"),
     Input("run-integration-btn", "n_clicks")],
    [State("radial-integrate-minval", "value"),
     State("radial-integrate-maxval", "value")],
)
def display_graph(n, l, integrate_click, rmin, rmax):
    """ This function produce the plot from the values of n and l and
    compute the integral, if the button is triggered """

    radial_part = AORadialPart(int(n), int(l))
    fig = radial_part.get_plot()

    if (rmin is not None and rmax is not None and
            callback_context.triggered[0]["prop_id"] == "run-integration-btn.n_clicks"):

        # display the area
        r = np.linspace(float(rmin), float(rmax), 400)
        Dr = r ** 2 * radial_part(r) ** 2
        fig.add_trace(
            go.Scatter(
                x=r, y=Dr, mode="lines", name="integration",
                fill="tozeroy", line=dict(color="#ff7f0e")
            )
        )

        # compute integration
        integral = np.trapz(Dr, x=r)

        result = [
            html.H4("Integration result"),
            html.P([
                dl.DashLatex(
                    rf"$P(e^-\in[{rmin:.1f}\;;\;{rmax:.1f}])$ = {integral:.2f}")
            ], style={"text-align": "center"})
        ]
        return fig, result

    else:
        message = [
            html.H4("Integration result"),
            html.P(
                "Click on compute the button to integrate the radial probability density.",
                style={"color": "Gray", "fontStyle": "italic", "fontWeight": 300}
            )
        ]
        return fig, message
