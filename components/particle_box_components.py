# coding: utf-8

from dash import html, dcc, callback, callback_context
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_latex as dl

from . import particle_box

""" This module implements the components for the particle in a box
(infinite well) tab. """

__author__ = "Germain Salvato Vallverdu"
__email__ = "germain.vallverdu@univ-pau.fr"

__all__ = ["text_doc", "selector"]

# parameter
P_MAX = 15
NPTS_MAX = 1000
NPTS_STEP = 10


# Documentation of this tab
# --------------------------
text_doc = [
    html.H3("Theory: Particle in a box"),
    dl.DashLatex(r"""Here, we consider the solutions of the 
        Schrödinger equation for a particle of mass $m$ in a box also 
        known as the infinite potential well. In such a case, the particle 
        is free to move on a segment of length $L$ : $x\in[0, L]$. 
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
    dl.DashLatex(r"""The respect of these conditions, leads to the 
        quantification of the energy characterized by a quantum number, 
        $p\in\mathbb{N}^*$. The solutions are labelled by this quantum number  
        $p$ and are the couples $(\phi_p, \varepsilon_p)$ including the 
        wavefunctions $\phi_p$ (the eigenvectors) and the energies 
        $\varepsilon_p$ (the eigenvalues). They read:"""),
    dl.DashLatex(r"""$$\begin{aligned}
            \phi_p(x) & = \sqrt{\frac{2}{L}} \sin\left(\frac{p\pi x}{L}\right) &
            \qquad\varepsilon_p & = \frac{h^2p^2}{8 m L^2}
        \end{aligned}$$""", displayMode=True),
]


def p_selector(title, base_id, value=1):
    return html.Div([
        html.H4("Select the quantum number: p"),
        html.Div([
            html.Button(
                html.Span(
                    className="fas fa-minus-square fa-3x",
                    style={"vertical-align": "top"}),
                id=f"{base_id}-minus-btn", n_clicks=0, className="pm-btn",
            ),
            html.Button(
                html.Span(
                    className="fas fa-plus-square fa-3x",
                    style={"vertical-align": "top"}),
                id=f"{base_id}-plus-btn", n_clicks=0, className="pm-btn",
            ),
            dl.DashLatex(title),
            html.Span(f"{value:3d}", id=f"{base_id}-number"),
        ],
            style={"display": "inline", "fontSize": "large"},
        )
    ])

def npts_selector(val_max, title, base_id, value=1, step=1, step_slider=5):
    return html.Div([
        html.H4(title),
        dcc.Slider(
            id=f"{base_id}-slider",
            min=1, max=val_max, step=1, value=value,
            marks={i: {"label": str(i)}
                    for i in range(1, val_max + step_slider, step_slider)},
            tooltip=dict(placement="bottom", always_visible=True)
        ),
    ])


def particle_box_tab():
    return dcc.Tab(
        label=" Particle in a box", className="fas fa-box custom-tab",
        value="particle-in-a-box",
        selected_className='custom-tab--selected',
        children=[
            html.Div(className="custom-tab-container", children=[
                dcc.Store(id="particle-in-a-box-data"),
                html.H3("Particle in a box system"),
                html.Div(children=[
                    # select p value
                    p_selector(base_id="p", title=r"$p=\;$"),
                    # select number of point
                    npts_selector(
                        NPTS_MAX, base_id="npts", value=100, step=NPTS_STEP,
                        step_slider=200, title="Number of points"),

                    #
                    html.Div([
                        html.H4("Wavefunction"),
                        html.Div([
                            daq.BooleanSwitch(id="show-wf", on=False),
                            html.P("Off", id="show-wf-text"),
                        ],
                            style={"display": "grid",
                                   "grid-template-columns": "50% 50%"}
                        ),
                    ]),

                    # replot button
                    html.Div([
                        html.H4("Replot"),
                        html.Button("run", id="replot-btn", n_clicks=0),
                    ],
                        style={"textAlign": "center"},
                    ),
                ],
                    style={"display": "grid",
                           "grid-template-columns": "30% 40% 15% 15%"}
                ),

                # plot
                html.Div(
                    dcc.Graph(id="particle-box-graph"),
                ),

                html.Div(className="docs", children=text_doc),
            ])
        ])


@callback(
    Output("p-number", "children"),
    [Input("p-plus-btn", "n_clicks"),
     Input("p-minus-btn", "n_clicks")],
    State("p-number", "children"),
)
def increase_p(click_plus, click_minus, p_str):
    ctx = callback_context
    p = int(p_str)

    if ctx.triggered[0]["prop_id"] == "p-plus-btn.n_clicks":
        if p < P_MAX:
            return f"{p + 1:2d}"
        else:
            return p_str

    elif ctx.triggered[0]["prop_id"] == "p-minus-btn.n_clicks":
        if p > 1:
            return f"{p - 1:2d}"
        else:
            return p_str

    else:
        return p_str


@callback(
    [Output("particle-box-graph", 'figure'),
     Output("show-wf-text", "children"),
     Output("particle-in-a-box-data", "data")],
    [Input("p-number", "children"),
     Input("npts-slider", "value"),
     Input("replot-btn", "n_clicks"),
     Input("show-wf", "on")],
    State("particle-in-a-box-data", "data"),
)
def display_graph(p_str, ntry, n_clicks, show_wf, data):
    """ This callback produce the plot from the sliders or the replot
    button. """

    ctx = callback_context

    # params
    p = int(p_str)
    L = 1
    jitter = .5

    # switch label
    text = "On" if show_wf else "Off"

    # replot from current data or not
    if ctx.triggered[0]["prop_id"] == "show-wf.on":
        # p and ntry did not change, just replot with or without wf
        fig = particle_box.plot(
            p, L=L, ntry=ntry, jitter=jitter, show_wf=show_wf,
            pos=data["pos"], pos_y=data["pos_y"]
        )
    else:
        # p or ntry changed, or replot => update data
        pos, pos_y = particle_box.compute_data(
            p, L=L, ntry=ntry, jitter=jitter)
        data = dict(pos=pos, pos_y=pos_y)
        fig = particle_box.plot(
            p, L=L, ntry=ntry, jitter=jitter, show_wf=show_wf,
            pos=pos, pos_y=pos_y
        )

    return fig, text, data
