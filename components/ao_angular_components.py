# coding: utf-8

from dash import html, dcc, callback
from dash.dependencies import Input, Output
import dash_latex as dl

from .ao_angular import angular_part_equations, angular_part_data, get_polar_plot

""" This module implements the components for the angular probability density tab """

__author__ = "Germain Salvato Vallverdu"
__email__ = "germain.vallverdu@univ-pau.fr"


# Documentation of this tab
# --------------------------
text_doc = [
    html.H3("Theory: Angular part of atomic orbitals"),
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
    html.P("""The angular part controls the shape and the space orientation
     of the atomic orbital. The angular part is represented by spherical 
     harmonic functions. The general expression reads"""),
    dl.DashLatex(r"""
    $$
        Y_{\ell}^{m-{\ell}} (\theta, \varphi) = 
        P_{\ell}^{m-{\ell}} (\theta) \exp(\pm i m_{\ell} \varphi)
    $$
    """, displayMode=True),
    dl.DashLatex(r"""where $P_{\ell}^{m-{\ell}} (\theta)$ is a Legendre
    polynom."""),
    dl.DashLatex(r"""Hereafter, are displayed the equations of the spherical
            harmonics for the lowest values of $\ell$ and $m_{\ell}$."""),
    dl.DashLatex(angular_part_equations, displayMode=True),
    dl.DashLatex(r"""The plots represent directly the spherical harmonic function
        not the probability density. The functions are plotted in the 
        $(xOz)$ plane, i.e. $\varphi=0$. The angles correspond to the $\theta$
        angles as defined in spherical coordinates. The vertical axes is
        the $\vec{z}$ axis and the horizontal axis is the $\vec{x}$ axis.""")
]


def angular_part_tab():
    return dcc.Tab(
        label=" Angular part of AO", className="far fa-globe custom-tab",
        value="AO-angular-part",
        selected_className='custom-tab--selected',
        children=[
            html.Div(className="custom-tab-container", children=[
                html.H3("Atomic orbitals - Shape of angular functions"),
                html.Div([
                    html.H4("Select the angular part:"),
                    html.Div([
                        # select n value
                        dcc.Dropdown(
                            options=[k for k in angular_part_data],
                            id="angular-part-dropdown",
                            # clearable=False,
                            placeholder="Select an angular part",
                            value="ns",
                        ),
                        html.Div(
                            id="angular-part-text",
                            className="docs",
                            style={"padding-left": "20px"})
                    ],
                        style={
                            "display": "grid",
                            "grid-template-columns": "30% 70%"
                    }
                    ),

                    # plot
                    dcc.Graph(id="angular-part-polar-graph"),
                ]),

                # docs
                html.Div(className="docs", children=text_doc),
            ])
        ])


@callback(
    [Output("angular-part-polar-graph", 'figure'),
     Output("angular-part-text", "children")],
    Input("angular-part-dropdown", "value"),
)
def display_graph(angular_part_name):
    """ This function produce the polar plot from the dropdown selection """

    text = [
        dl.DashLatex(angular_part_data[angular_part_name]["text"]),
    ]

    return get_polar_plot(angular_part_name), text
