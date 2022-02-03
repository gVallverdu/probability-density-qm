#!/usr/bin/env python
# coding: utf-8

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html
import dash_latex as dl

from infinite_well import phi, infinite_well_plot

# Set up app
# ------------------------------------------------------------------------------
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Probability density - Quantum chemistry"

TITLE = "Probability density of a particle in a box"
URL = "https://github.com/gVallverdu/probability-density-qm"

# parameter
P_MAX = 15
NPTS_MAX = 1000
NPTS_STEP = 10


# Plot tab:
#     controls of the plot
#     the plot
# ------------------------------------------------------------------------------
plot_tab = dcc.Tab(
    label=" Plot", className="fas fa-chart-area custom-tab",
    selected_className='custom-tab--selected',
    # labelClassName="fas fa-chart-area",
    children=[html.Div(className="custom-tab-container", children=[
        html.Div(children=[
            # html.Div(className="four columns", children=[
            html.Div([
                html.H4("Value of the quantum number p"),
                html.Div([
                    html.Button(
                        html.Span(className="fas fa-minus-square fa-3x"),
                        id="p-minus-btn", n_clicks=0, className="pm-btn",
                        style={"textAlign": "right"}
                    ),
                    dcc.Slider(
                        id='p-slider',
                        min=1, max=P_MAX, step=1, value=1,
                        marks={i: {"label": str(i)}
                                for i in range(0, P_MAX + 5, 5)},
                        tooltip=dict(placement="bottom",
                                        always_visible=True)
                    ),
                    html.Button(
                        html.Span(className="fas fa-plus-square fa-3x"),
                        id="p-plus-btn", n_clicks=0, className="pm-btn",
                        style={"textAlign": "left"}
                    )],
                    style={"display": "grid", "grid-template-columns": "15% 70% 15%"}
                ),
            ]),
            # html.Div(className="four columns", children=[
            html.Div([
                html.H4("Number of points"),
                html.Div([
                    html.Button(
                        html.Span(className="fas fa-minus-square fa-3x"),
                        id="npts-minus-btn", n_clicks=0, className="pm-btn",
                        style={"textAlign": "right"}
                    ),
                    dcc.Slider(
                        id='npts-slider',
                        min=1, max=NPTS_MAX, step=NPTS_STEP, value=100,
                        marks={i: {"label": str(i)} for i in range(
                            0, NPTS_MAX + 200, 200)},
                        tooltip=dict(placement="bottom",
                                        always_visible=True)
                    ),
                    html.Button(
                        html.Span(className="fas fa-plus-square fa-3x"),
                        id="npts-plus-btn", n_clicks=0, className="pm-btn",
                        style={"textAlign": "left"}
                    ),],
                    style={"display": "grid", "grid-template-columns": "15% 75% 15%"}
                ),
            ]),
            # html.Div(className="two columns", children=[
            html.Div([
                html.H4("Wavefunction"),
                dcc.RadioItems(
                    id="show_wf",
                    options=[
                        dict(label="Show", value="Show"),
                        dict(label="Hide", value="Hide"),
                    ],
                    value="Hide",
                    labelStyle={'display': 'inline-block'},
                    inputStyle={"margin-left": "10px"}
                ),
            ]),
            # html.Div(className="two columns", children=[
            html.Div([
                html.H4("Replot"),
                html.Button(
                    "run", id="replot-btn", n_clicks=0
                ),
            ]),
        ],
        style={"display": "grid", "grid-template-columns": "35% 35% 20% 10%"}
        ),
        # a place for the plot
        html.Div(
            dcc.Graph(id='graph'),
        ),
    ])
    ])

doc_tab = dcc.Tab(
    label=" Documentation",
    # labelClassName="fas fa-file-alt",
    className="fas fa-file-alt custom-tab",
    selected_className='custom-tab--selected',
    children=[
        html.Div(className="custom-tab-container docs", children=[
            dl.DashLatex(r"""Here, we consider the solutions of the 
        Schrödinger equation for a particle of mass $m$ in a box also known as 
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
            dl.DashLatex(r"""The solutions are the couples, identified
        by the quantum number $p\in\mathbb{N}^*$, associating 
        the wavefunctions $\phi_p$ (the eigenvectors) and the energies $\varepsilon_p$
        (the eigenfunctions). They read:"""),
            dl.DashLatex(r"""$$\begin{aligned}
        \phi_p(x) & = \sqrt{\frac{2}{L}} \sin\left(\frac{p\pi x}{L}\right) &
        \qquad\varepsilon_p & = \frac{h^2p^2}{8 m L^2}
        \end{aligned}$$""", displayMode=True),
        ]),
    ])

# HTML page Layout
# ----------------
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
        html.H3(className="tab-title", children=TITLE),
        dcc.Tabs([plot_tab, doc_tab]),
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
     Input("replot-btn", "n_clicks"),
     Input("show_wf", "value")],
)
def display_graph(p, ntry, n_clicks, show_wf):
    """ This function produce the plot from the sliders or the replot
    button. """

    # params
    L = 1
    nbins = 30
    jitter = .5

    return infinite_well_plot(p, L=L, ntry=ntry, nbins=nbins,
                              jitter=jitter, show_wf=show_wf)


@app.callback(
    Output("p-slider", "value"),
    [Input("p-plus-btn", "n_clicks"),
     Input("p-minus-btn", "n_clicks")],
    State("p-slider", "value"),
)
def increase_p(click_plus, click_minus, p):
    ctx = dash.callback_context

    if ctx.triggered[0]["prop_id"] == "p-plus-btn.n_clicks":
        if p < P_MAX:
            return p + 1
        else:
            return p

    elif ctx.triggered[0]["prop_id"] == "p-minus-btn.n_clicks":
        if p > 1:
            return p - 1
        else:
            return p

    else:
        return p


@app.callback(
    Output("npts-slider", "value"),
    [Input("npts-plus-btn", "n_clicks"),
     Input("npts-minus-btn", "n_clicks")],
    State("npts-slider", "value"),
)
def increase_p(click_plus, click_minus, npts):
    ctx = dash.callback_context

    if ctx.triggered[0]["prop_id"] == "npts-plus-btn.n_clicks":
        if npts < NPTS_MAX:
            return npts + NPTS_STEP
        else:
            return npts

    elif ctx.triggered[0]["prop_id"] == "npts-minus-btn.n_clicks":
        if npts > NPTS_STEP:
            return npts - NPTS_STEP
        else:
            return npts

    else:
        return npts


if __name__ == '__main__':
    app.run_server(debug=False, host='127.0.0.1')
