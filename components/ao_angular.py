#!/usr/bin/env python
# coding: utf-8

import numpy as np
import plotly.graph_objects as go


""" This module implements spherical harmonics be considered in the
application. 

Only real functions are considered. Real functions can be obtained 
from the linear combination of spherical harmonic with the same value
of l and the same absolute value of m_l. For example:

$$
    \frac{1}{\sqrt 2} \left(-Y_1^1 + Y_1^{-1}\right) = \sqrt{\frac{3}{2\pi}} \sin\theta\cos\varphi
$$
"""

__author__ = "Germain Salvato Vallverdu"
__email__ = "germain.vallverdu@univ-pau.fr"

L_MAX = 3

angular_part_equations = r"""$$\begin{aligned}
    Y_0^0 & = \frac{1}{\sqrt{4\pi}} \\
    Y_1^0 & = \sqrt{\frac{3}{4\pi}} \cos\theta & 
    Y_1^{\pm1} & = \mp\sqrt{\frac{3}{2\pi}} \sin\theta \, e^{\pm i\varphi} \\
    Y_2^0 & = \sqrt{\frac{5}{16\pi}} \left(3\cos^2\theta-1\right) &
    Y_2^{\pm 1} & = \mp \sqrt{\frac{15}{4\pi}} \sin\theta\cos\theta \, e^{\pm i\varphi} &
    Y_2^{\pm 2} & = \sqrt{\frac{15}{4\pi}} \sin^2\theta \, e^{\pm 2i\varphi} \\
    Y_3^0 & = \sqrt{\frac{7}{16\pi}} \left(5\cos^3\theta - 3\cos\theta\right) &
    Y_3^{\pm 1} & = \mp \sqrt{\frac{21}{64\pi}} \sin\theta\left(5\cos^2\theta - 1\right) \, e^{\pm i\varphi} &
    Y_3^{\pm 2} & = \sqrt{\frac{105}{16\pi}} \sin^2\theta\cos\theta \, e^{\pm 2i\varphi} \\
    & & & & Y_3^{\pm 3} & = \mp \sqrt{\frac{35}{64\pi}} \sin^3\theta \, e^{\pm 3i\varphi}
\end{aligned}$$"""

# Real spherical harmonics
# ------------------------


def Y00(theta, phi):
    """ spherical harmonic """
    return 1 / np.sqrt(4 * np.pi)


def Y10(theta, phi):
    """ Y_1^0 function: OA pz """
    return np.sqrt(3 / (4 * np.pi)) * np.cos(theta)


def Y20(theta, phi):
    """ Y_2^0 function: OA dz2 """
    return np.sqrt(5 / (16 * np.pi)) * (3 * np.cos(theta)**2 - 1)


def Y30(theta, phi):
    """ Y_3^0 function: OA fz3 """
    return np.sqrt(7 / (16 * np.pi)) * (5 * np.cos(theta)**3 - 3 * np.cos(theta))


def Y11x(theta, phi):
    """ Linear combination to get a real function associated to a px AO
        1 / sqrt(2) (-Y_1^1 + Y_1^-1) """
    return np.sqrt(3 / (4 * np.pi)) * np.sin(theta) * np.cos(phi)


def Y21xz(theta, phi):
    """ Linear combination to get a real function associated to a dxz AO
    1 / sqrt(2) (-Y_2^1 + Y_2^-1) """
    return np.sqrt(15 / (2 * np.pi)) * np.sin(theta) * np.cos(theta) * np.cos(phi)


def Y31xz2(theta, phi):
    """ Linear combination to get a real function associated to a fxz2 AO
    1 / sqrt(2) (-Y_3^1 + Y_3^-1) """
    return np.sqrt(21 / (32 * np.pi)) * np.sin(theta) * (5 * np.cos(theta)**2 - 1) * np.cos(phi)


# links between l, m_l values and spherical harmonics
angular_functions = {
    (0, 0): dict(function=Y00, value="ns", label=r"$ns$"),
    (1, 0): dict(function=Y10, value="npz", label=r"$np_z$"),
    (1, 1): dict(function=Y11x, value="npx", label=r"$np_x$"),  # this is arbitrary
    (2, 0): dict(function=Y20, value="ndz2", label=r"$nd_{z^2}$"),
    (2, 1): dict(function=Y21xz, value="ndxy", label=r"$nd_{xz}$"),
    (3, 0): dict(function=Y30, value="nfz3", label=r"$nf_{z^3}$"),
    (3, 1): dict(function=Y31xz2, value="nfxz2", label=r"$nf_{xz^2$"),
}

angular_part_data = {
    "ns": dict(
        function=Y00, nodal_angles=[], label=r"$ns$",
        l_m_l=(0, 0),
        text=r"AO $ns$ with function $Y_{0}^{0}(\theta, \varphi)$: $\ell = 0$ and $m_{\ell}=0$, no nodal plane."
        # text=[r"AO $ns$ with function $Y_{0}^{0}(\theta, \varphi)$", r"$\ell = 0$ and $m_{\ell}=0$", r"no nodal plane."]
    ),
    "npz": dict(
        function=Y10, label=f"$np_z", nodal_angles=[np.pi / 2],
        l_m_l=(1, 0),
        text=r"AO $np_z$ with function $Y_{1}^{0}(\theta, \varphi)$: $\ell = 1$ and $m_{\ell}=0$, 1 nodal plane."
        # text=[r"AO $np_z$ with function $Y_{1}^{0}(\theta, \varphi)$", r"$\ell = 1$ and $m_{\ell}=0$", r"$1$ nodal plane."]
    ),
    "npx": dict(
        function=Y11x, nodal_angles=[0], value=r"$np_x$",
        l_m_l=(1, 1), label=r"$np_x$",
        text=(r"AO $np_x$ with function "
              r"$\frac{1}{\sqrt{2}}\Big(Y_{1}^{1}(\theta, \varphi) + Y_{1}^{-1}(\theta, \varphi)\Big)$"
              r": $\ell = 1$ and $m_{\ell}=\pm 1$, 1 nodal plane.")
    ),
    "ndz2": dict(
        function=Y20,
        label=r"$nd_{z^2}$",
        l_m_l=(2, 0),
        nodal_angles=[np.arccos(1 / np.sqrt(3)), -np.arccos(1 / np.sqrt(3))],
        text=r"AO $nd_{z^2}$ with function $Y_{2}^{0}(\theta, \varphi)$: $\ell = 2$ and $m_{\ell}=0$, 2 nodal planes."
    ),
    "ndxy": dict(
        function=Y21xz,
        l_m_l=(2, 1),
        label=r"$nd_{xz}$",
        nodal_angles=[0, np.pi / 2],
        text=(r"AO $nd_{xz}$ with function "
              r"$\frac{1}{\sqrt{2}}\Big(Y_{2}^{-1}(\theta, \varphi) - Y_{2}^{1}(\theta, \varphi)\Big)$"
              r": $\ell = 2$ and $m_{\ell}=\pm 2$, 2 nodal planes.")
    ),
    "nfz3": dict(
        function=Y30,
        l_m_l=(3, 0),
        label=r"$nf_{z^3}$",
        nodal_angles=[np.pi / 2,
                      np.arccos(np.sqrt(3 / 5)), -np.arccos(np.sqrt(3 / 5))],
        text=r" AO $nf_{z^3}$ with function $Y_{3}^{0}(\theta, \varphi)$: $\ell = 3$ and $m_{\ell}=0$, 3 nodal planes."
    ),
    "nfxz2": dict(
        function=Y31xz2,
        l_m_l=(3, 1),
        label=r"$nf_{xz^2$",
        nodal_angles=[0, np.arccos(np.sqrt(1/5)), -np.arccos(np.sqrt(1/5))],
        text=(r"AO $nf_{xz^2}$ with function "
              r"$\frac{1}{\sqrt{2}}\Big(Y_{3}^{-1}(\theta, \varphi) - Y_{3}^{1}(\theta, \varphi)\Big)$"
              r": $\ell = 2$ and $m_{\ell}=\pm 1$, 3 nodal planes.")
    ),
}


# A wrapper over spherical harmonics
# ----------------------------------


def are_l_m_l_valid(l, m_l):
    """ Check of l and m_l values are valid

    Args:
        l (int): secondary quantum number
        m_l (int): magnetic quantum number
    """
    try:
        l = int(l)
    except ValueError as e:
        print(e)
        raise ValueError(f"l must be an integer. l = '{l}'.")
    if not 0 <= l <= L_MAX:
        raise ValueError(f"l must be in [0, 3]. l = {l}.")

    try:
        m_l = int(m_l)
    except ValueError as e:
        print(e)
        raise ValueError(f"m_l must be an integer. m_l = '{m_l}'.")
    if not -l <= m_l <= l:
        raise ValueError(f"m_l must be in [{-l}, {l}]. m_l = {m_l}.")

    return True


def angular(theta, phi=0, l=0, m_l=0):
    """ Select an atomic orbital depending on l and m_l quantum numbers

    Args:
        theta (float): theta angle of spherical coordinates
        phi (float): phi angle of spherical coordinates
        l (int): secondary quantum number
        m_l (int): magnetic quantum number
    """

    return angular_functions[(l, m_l)](theta, phi)

# A wrapper over spherical harmonics
# ----------------------------------


def get_polar_plot(name="ns", step=1, show_wf=True):
    """ Produce a plotly figure with polar axes in the (x, z) plane 

    Args:
        name (str): Name of the angular part
        step (int, float): step for theta values range
        show_wf (bool): if True, show the wavefunction, else show the angular density
    """

    # get l, m_l values
    l, m_l = angular_part_data[name]["l_m_l"]

    # compute r, theta values
    theta = np.radians(np.arange(0, 360 + step, step))

    # compute wavefunction
    wf = angular_part_data[name]["function"](theta, phi=0)
    if name == "ns":
        wf = np.ones(theta.shape) * wf

    if show_wf:
        angular_values = wf
        maxval = np.max(np.abs(angular_values))
    else:
        angular_values = wf ** 2
        maxval = np.max(angular_values)

    # split positive and negative part
    ix_p = np.where(angular_values >= 0)
    ix_n = np.where(angular_values < 0)

    r_range = [0, 1.1 * maxval]
    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=np.abs(angular_values[ix_n]),
            theta=theta[ix_n],
            thetaunit="radians",
            mode='lines',
            line=dict(color="SteelBlue"),
            fill="toself",
            fillcolor="rgba(70, 130, 180, .25)",
            name="negative part"
        )
    )

    if show_wf:
        pos_name = "positive part"
    else:
        pos_name = "Probability density"

    fig.add_trace(
        go.Scatterpolar(
            r=angular_values[ix_p],
            theta=theta[ix_p],
            thetaunit="radians",
            mode='lines', fill="toself", fillcolor="rgba(178, 34, 34, .25)",
            line=dict(color="FireBrick"),
            name=pos_name,
        )
    )

    for i, nodal_angle in enumerate(angular_part_data[name]["nodal_angles"]):
        showlegend = True if i == 0 else False

        fig.add_trace(
            go.Scatterpolar(
                r=2 * r_range, theta=2 * [nodal_angle] + 2 * [nodal_angle + np.pi],
                thetaunit="radians", mode="lines", line=dict(color="DarkOrange"),
                name="nodal plane", hovertext="nodal plane", hoverinfo="skip",
                showlegend=showlegend,
            )
        )

    fig.update_layout(
        showlegend=True,
        legend=dict(xanchor="right"),
        height=800,
        title="Representation of the spherical harmonic in the (xOz) plane.",
        polar=dict(
            angularaxis=dict(
                tickfont_size=20, rotation=90, direction="clockwise",
                gridcolor="LightGray", tickmode="array", tickvals=list(range(0, 360, 30)),
                showline=True, linecolor="Gray", linewidth=2, gridwidth=2,
            ),
            radialaxis=dict(
                gridcolor="LightGray", showgrid=True, showline=False,
                range=r_range,
            ),
            bgcolor="white",
        ),
    )

    return fig
