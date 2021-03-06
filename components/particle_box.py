#!/usr/bin/env python
# coding: utf-8

import numpy as np
from scipy.constants import h, m_e, elementary_charge

import plotly.graph_objects as go
from plotly.subplots import make_subplots

""" This module implements wave functions to be considered in the
application in the case of the particle in a box system. """

__author__ = "Germain Salvato Vallverdu"
__email__ = "germain.vallverdu@univ-pau.fr"


def phi(x, p=1, L=1):
    """ Wavefunction solution of the infinite well system

    Args:
        p (int): quantum number
        m (float): particle mass
        L (float): width of the well 
    """
    return np.sqrt(2 / L) * np.sin(p * np.pi * x / L)


def epsilon(p, m=m_e, L=1):
    """ Energy associated to the wavefunction of the infinite well system.

    Args:
        p (int): quantum number
        m (float): particle mass
        L (float): width of the well

    Returns
        energy in eV
    """
    return h**2 * p**2 / (8 * m * L**2) / elementary_charge


def sample(ntry=100, p=1, L=1):
    """ Draw ntry points from the probability density associated to 
    the infinit well.
    """
    n = 0
    pos = list()
    while n < ntry:
        x = np.random.uniform(0, L)
        rho = phi(x, p, L)**2
        if rho > np.random.uniform(0, 2 / L):
            n += 1
            pos.append(x)
    return pos


def compute_data(p=1, L=1, ntry=100, jitter=.5):
    """ 
    This function produce a plot with the probability density and an
    histogram of the position drawn from this density. The points are
    depicted in a subplot with a random dispersion on the vertical 
    direction.

    Args:
        p (int): the quatum number
        L (float): the length of the box
        ntry (int): the number of sampled points
        jitter (float): dispersion along y for points representation

    Returns:
        pos and pos_y, the (x, y) coordinates of points
    """
    pos = sample(ntry, p, L)
    pos_y = np.random.normal(0, jitter, ntry)

    return pos, pos_y


def plot(p=1, L=1, ntry=100, jitter=.5, show_wf=False, pos=None, pos_y=None):
    """ 
    This function produce a plot with the probability density and an
    histogram of the position drawn from this density. The points are
    depicted in a subplot with a random dispersion on the vertical 
    direction.

    Args:
        p (int): the quatum number
        L (float): the length of the box
        ntry (int): the number of sampled points
        jitter (float): dispersion along y for points representation
        show_wf (bool): if True the wavefunction is plotted

    Returns:
        A plotly figure object
    """

    # data
    x = np.linspace(0, L, 500)

    if pos is None or pos_y is None:
        pos, pos_y = compute_data(p, L, ntry, jitter)

    # fig = go.Figure()
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        horizontal_spacing=0, vertical_spacing=0,
        row_heights=[0.75, 0.25],
    )

    fig.add_trace(go.Histogram(
        x=pos,
        opacity=.4,
        histnorm="probability density",
        marker_color="#1f77b4",
        name="histogram",
    ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=x, y=phi(x, p, L) ** 2,
            mode="lines",
            name="probability density",
            line=dict(color="#d62728")
        ),
        row=1, col=1,
    )

    fig.add_hline(y=0, line=dict(color="#7f7f7f"), row=1, col=1)

    fig.add_trace(
        go.Scatter(
            x=pos, y=pos_y,
            mode="markers",
            marker_color="#7f7f7f",
            opacity=.6,
            showlegend=False,
            hoverinfo="skip"
        ),
        row=2, col=1,
    )

    if p > 1:
        nodes = [(i * L / p, 0) for i in range(1, p)]
        fig.add_trace(
            go.Scatter(
                x=[v[0] for v in nodes],
                y=[v[1] for v in nodes],
                mode="markers",
                marker_color="#ff7f0e",
                marker_size=15,
                name="nodes",
                hoverinfo="skip",
                # showlegend=False,

            )
        )

    if show_wf:
        fig.add_trace(
            go.Scatter(
                x=x, y=phi(x, p, L),
                mode="lines",
                name="wavefunction",
                line=dict(color="#2ca02c")
            ),
            row=1, col=1,
        )

    fig.update_xaxes(
        showticklabels=True,
        fixedrange=True,
        title="x (A)",
        row=2, col=1
    )

    # avoid zooming capabilities
    fig.update_xaxes(fixedrange=True, row=1, col=1)
    fig.update_yaxes(fixedrange=True, row=1, col=1)

    fig.update_yaxes(
        fixedrange=True,
        showticklabels=False,
        title=f"sample points <br> npts = {ntry}",
        range=[-8 * jitter, 8 * jitter],
        row=2, col=1
    )

    fig.update_layout(
        title=f"Particle in a box wavefunctions: p = {p}",
        autosize=True,
        # width=800,
        height=600,
        yaxis_title="Probability density",
        xaxis=dict(range=[0, L]),
        bargap=.1,
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(xanchor="right",)
    )

    return fig
