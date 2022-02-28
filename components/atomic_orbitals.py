#!/usr/bin/env python
# coding: utf-8

import numpy as np
import plotly.graph_objects as go

from . import ao_angular
from .ao_radial import AORadialPart

from scipy.constants import physical_constants, angstrom
BOHR_RADIUS = physical_constants["Bohr radius"][0] / angstrom


""" This module implements functions to compute atomic orbitals 
combining radial and angular part. """

__author__ = "Germain Salvato Vallverdu"
__email__ = "germain.vallverdu@univ-pau.fr"


def sample(ao_function, rmax=15, ntry=10000, phi=0):
    """ Sample the AO function in the x z plane from cartesian coordinates.

    The density is not perfectly True but it is enough for visualizing the
    electronic cloud.
    """

    npts = 0
    points = list()
    wf = list()
    while npts < ntry:
        x = np.random.uniform(-rmax, rmax, ntry)
        z = np.random.uniform(-rmax, rmax, ntry)
        r = np.sqrt(x ** 2 + z ** 2)
        theta = np.arccos(z / r)  # theta from spherical coordinate

        wf_i = ao_function(r, theta, phi=phi)
        rho = wf_i ** 2
        rnd = np.random.uniform(0, rho.max(), ntry)
        ix = np.where(rho > rnd)
        points_i = np.concatenate(
            [x[ix[0], np.newaxis], z[ix[0], np.newaxis]], axis=1)
        wf_i = wf_i[ix]

        npts += wf_i.size
        points.append(points_i)
        wf.append(wf_i)

    points = np.concatenate(points)
    wf = np.concatenate(wf)

    return points, wf

# spheric symmetry atomic orbitals


def OA1s(r, theta, phi, ao=BOHR_RADIUS, Z=1):
    """ 1s atomic orbital """
    return AORadialPart.radial1s(r, Z, ao) * ao_angular.Y00(theta, phi)


def OA2s(r, theta, phi, ao=BOHR_RADIUS, Z=1):
    """ 2s atomic orbital """
    return AORadialPart.radial2s(r, Z, ao) * ao_angular.Y00(theta, phi)


def OA3s(r, theta, phi, ao=BOHR_RADIUS, Z=1):
    """ 3s atomic orbital """
    return AORadialPart.radial3s(r, Z, ao) * ao_angular.Y00(theta, phi)


# higher orbital moment

def OA2pz(r, theta, phi, ao=BOHR_RADIUS, Z=1):
    """ 2pz atomic orbital """
    return AORadialPart.radial2p(r, Z, ao) * ao_angular.Y10(theta, phi)


def OA3pz(r, theta, phi, ao=BOHR_RADIUS, Z=1):
    """ 3pz atomic orbital """
    return AORadialPart.radial3p(r, Z, ao) * ao_angular.Y10(theta, phi)


def OA3dz2(r, theta, phi, ao=BOHR_RADIUS, Z=1):
    """ 3dz2 atomic orbital """
    return AORadialPart.radial3d(r, Z, ao) * ao_angular.Y20(theta, phi)


def OA4fz3(r, theta, phi, ao=BOHR_RADIUS, Z=1):
    """ 4fz3 atomic orbital """
    return AORadialPart.radial4f(r, Z, ao) * ao_angular.Y30(theta, phi)


ao_data = {
    "1s": dict(function=OA1s, nodal_angles=[], nodal_r=[], rmax=3),
    "2s": dict(function=OA2s, nodal_angles=[], nodal_r=[2 * BOHR_RADIUS], rmax=10),
    "3s": dict(
        function=OA3s,
        nodal_angles=[],
        nodal_r=[
            3 * BOHR_RADIUS / 2 * (3 + np.sqrt(3)),
            3 * BOHR_RADIUS / 2 * (3 - np.sqrt(3))
        ],
        rmax=15,
    ),
    "2pz": dict(function=OA2pz, nodal_angles=[np.pi / 2], nodal_r=[], rmax=10),
    "3pz": dict(function=OA3pz, nodal_angles=[np.pi / 2], nodal_r=[6 * BOHR_RADIUS], rmax=15),
    "3dz2": dict(
        function=OA3dz2,
        nodal_angles=[np.arccos(1 / np.sqrt(3)), -np.arccos(1 / np.sqrt(3))],
        nodal_r=[],
        rmax=15,
    ),
    "4fz3": dict(
        function=OA4fz3,
        nodal_angles=[np.pi / 2,
                      np.arccos(np.sqrt(3 / 5)), -np.arccos(np.sqrt(3 / 5))],
        nodal_r=[],
        rmax=15,
    ),
}


def get_plot(ao_name, points=None, wf=None, ntry=1000, show_sign=False,
             show_nodal=True):
    """ Make the plot """

    # ao function
    ao_function = ao_data[ao_name]["function"]

    if points is None:
        rmax = ao_data[ao_name]["rmax"]
        points, wf = sample(ao_function, rmax=rmax, ntry=ntry, phi=0)

    # produce figure
    fig = go.Figure()
    rlim = 15

    if show_sign:
        ix = np.where(wf > 0)
        mask = np.ones(points.shape[0], dtype=bool)
        mask[ix] = False

        fig.add_trace(go.Scatter(
            x=points[~mask, 0], y=points[~mask, 1],
            mode="markers",
            marker_color="Firebrick",
            opacity=.6,
            showlegend=True,
            hoverinfo="skip",
            name="positive part",
        ))

        fig.add_trace(go.Scatter(
            x=points[mask, 0], y=points[mask, 1],
            mode="markers",
            marker_color="SteelBlue",
            opacity=.6,
            showlegend=True,
            hoverinfo="skip",
            name="negative part",
        ))

    else:
        fig.add_trace(go.Scatter(
            x=points[:, 0], y=points[:, 1],
            mode="markers",
            marker_color="#7f7f7f",
            opacity=.6,
            name="density",
            showlegend=True,
            hoverinfo="skip"
        ))

    # draw nodal planes
    if show_nodal:
        radius = ao_data[ao_name]["nodal_r"]
        theta = np.linspace(0, 2 * np.pi, 400)
        for i, r in enumerate(radius):
            showlegend = True if i == 0 else False
            fig.add_trace(go.Scatter(
                x=r * np.cos(theta), y=r * np.sin(theta),
                mode="lines",
                showlegend=showlegend,
                name="radial nodal plane",
                hoverinfo="skip",
                line=dict(color="DarkOrange")
            ))

        angles = ao_data[ao_name]["nodal_angles"]
        for i, angle in enumerate(angles):
            showlegend = True if i == 0 else False
            x = [-rlim, rlim]
            angle = angle + np.pi if angle < 0 else angle
            y = [-rlim / np.tan(angle), rlim / np.tan(angle)]
            fig.add_trace(go.Scatter(
                x=x, y=y,
                mode="lines",
                showlegend=showlegend,
                name="angular nodal plane",
                hoverinfo="skip",
                line=dict(color="DarkOrange", dash="dash")
            ))

    # update figure layout
    fig.update_layout(
        height=700,
        plot_bgcolor="white",
        xaxis=dict(
            gridcolor="LightGray", range=[-rlim, rlim],
            zeroline=True, zerolinecolor="LightGray", zerolinewidth=2,
            title_text="x (A)",
        ),
        yaxis=dict(
            gridcolor="LightGray", range=[-rlim, rlim],
            zeroline=True, zerolinecolor="LightGray", zerolinewidth=2,
            scaleanchor="x", scaleratio=1,
            title_text="z (A)",
        ),
        legend=dict(
            xanchor="right", yanchor="bottom",
            orientation="h", x=1, y=1.02,
        ),
    )

    return fig
