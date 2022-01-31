#!/usr/bin/env python
# coding: utf-8

import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import dash_latex as dl

from infinite_well import infinite_well_plot

# Set up app
# ------------------------------------------------------------------------------
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

TITLE = "Probability density of a particle in a box"
URL = "https://github.com/gVallverdu/probability-density-qm"

# HTML page Layout
# ------------------------------------------------------------------------------
# Page is divided in three parts:
#    * header: at the top, a title
#    * body: the main containt
#    * footer: at the bottom, contact, informations, credits
app.layout = html.Div(className="container", children=[
    html.Div(id="github-div", children=[
        html.A(
            id="github-link",
            href=URL,
            children=[
                html.Span(
                    id="github-icon", className="fab fa-github fa-2x",
                    style={"verticalAlign": "bottom"}),
                    " View on GitHub"])
    ]),

    # ----- body
    html.Div([
        html.H2(className="tab-title", children=TITLE),
        html.Div(children=[
            dl.DashLatex(r"""Hereafter, we consider the solutions of the 
            Shcrödinger equation for a particle in a box also known as 
            the infinite potential well. In such a case, the particle is 
            free to move on a segment of length $L$ : $x\in[0, L]$. 
            The Schrödinger equation reads"""),
            dl.DashLatex(r"""$$\begin{aligned}
             \hat{\mathcal{H}} \phi  & = \varepsilon\phi &
            \qquad-\frac{\hbar^2}{2m}\frac{d^2\phi}{dx^2} & = \varepsilon \phi
            \end{aligned}$$""", displayMode=True),
            html.P("""The solutions of the Schrödinger equation have to
                satisfy the following boundary conditions along with the 
                normalisation condition:"""),
            dl.DashLatex(r"""$$\begin{aligned}\begin{cases}
                \phi(0) & = 0 \\
                \phi(L) & = 0 \\
                \end{cases} & &
                \qquad\int_0^L \left\vert\phi(x)\right\vert^2 dx & = 1
            \end{aligned}$$""", displayMode=True),
            dl.DashLatex(r"""The solutions are the couples associating 
            the wavefunctions $\phi_p$ and the energies $\varepsilon_p$
            (the eigenfunctions and the eigenvectors) and read:"""),
            dl.DashLatex(r"""$$\begin{aligned}
            \phi_p(x) & = \sqrt{\frac{2}{L}} \sin\left(\frac{p\pi x}{L}\right) &
            \qquad\varepsilon_p & = \frac{h^2p^2}{8 m L^2}
            \end{aligned}$$""", displayMode=True),
        ]),

        html.Div(className="row", children=[
            html.Div(className="five columns", children=[
                html.H4("Value of the quantum number p"),
                dcc.Slider(
                    id='p-slider',
                    min=1, max=20, step=1, value=1,
                    marks={i: {"label": str(i)} for i in [1, 5, 10, 15, 20]},
                    tooltip=dict(placement="bottom", always_visible=True)
                ),
            ]),
            html.Div(className="five columns", children=[
                html.H4("Number of points"),
                dcc.Slider(
                    id='npts-slider',
                    min=1, max=2000, step=10, value=100,
                    marks={i: {"label": str(i)} for i in range(0, 2250, 250)},
                    tooltip=dict(placement="bottom", always_visible=True)
                ),
            ]),
            html.Div(className="two columns", children=[
                html.H4("Run"),
                html.Button(
                    "Replot", id="replot-btn", n_clicks=0
                ),
            ])
        ]),

        # a place for the plot with an id
        html.Div(
            dcc.Graph(id='graph'),
        ),
    ]),

    # ----- footer
    html.Div(className="footer", children=[
        html.Div(className="row", children=[
            html.Div(className="six columns", children=[
                html.A(
                    html.Img(
                        src="http://gvallver.perso.univ-pau.fr/img/logo_uppa.png",
                        height="50px",
                    ),
                    href="https://www.univ-pau.fr"
                )
            ]),
            html.Div(className="six columns", children=[
                html.P(children=[
                    html.A("Germain Salvato Vallverdu",
                            href="https://gsalvatovallverdu.gitlab.io",
                            style={"color": "#7f8c8d"})
                ]),
            ], style={"textAlign": "right", "paddingTop": "10px"})
        ]),
    ]),
])

# Callback functions => interactivity
# Each element on the page is identified thanks to its `id`
# ------------------------------------------------------------------------------


@app.callback(
    Output('graph', 'figure'),
    [Input("p-slider", "value"),
     Input("npts-slider", "value"),
     Input("replot-btn", "n_clicks")],
)
def display_graph(p, ntry, n_clicks):
    """ This function produce the plot from the sliders or the replot
    button. """

    return infinite_well_plot(p, L=1, ntry=ntry, nbins=30, jitter=.5)


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
