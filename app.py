#!/usr/bin/env python
# coding: utf-8

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html

from components import header, footer
from infinite_well import infinite_well_plot, text_doc

# Set up app
# ------------------------------------------------------------------------------
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Probability density - Quantum chemistry"

TITLE = "Probability density - Quantum chemistry"
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
    children=[html.Div(className="custom-tab-container", children=[
        html.Div(children=[
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
                    style={"display": "grid",
                           "grid-template-columns": "15% 70% 15%"}
                ),
            ]),
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
                    ), ],
                    style={"display": "grid",
                           "grid-template-columns": "15% 75% 15%"}
                ),
            ]),
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
            html.Div([
                html.H4("Replot"),
                html.Button(
                    "run", id="replot-btn", n_clicks=0
                ),
            ]),
        ],
            style={"display": "grid", "grid-template-columns": "35% 35% 20% 10%"}
        ),
        html.Div(
            dcc.Graph(id='graph'),
        ),
    ])
    ])

# Doc tab:
#     provide explications
# ------------------------------------------------------------------------------
doc_tab = dcc.Tab(
    label=" Documentation",
    className="fas fa-file-alt custom-tab",
    selected_className='custom-tab--selected',
    children=[
        html.Div(className="custom-tab-container docs", children=text_doc),
    ])

# HTML page Layout
# ----------------
app.layout = html.Div(className="container", children=[
    header(TITLE, URL, fa_icon="fas fa-atom"),

    # ----- body
    html.Div([
        html.H3(className="tab-title", children=TITLE),
        dcc.Tabs([plot_tab, doc_tab]),
    ]),

    # ----- footer
    footer(
        logo_img="http://gvallver.perso.univ-pau.fr/img/logo_uppa.png",
        logo_url="https://www.univ-pau.fr"
    ),
])

# Callback functions => interactivity
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
    jitter = .5

    return infinite_well_plot(p, L=L, ntry=ntry, jitter=jitter, show_wf=show_wf)


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
    app.run_server(debug=True, host='127.0.0.1')
