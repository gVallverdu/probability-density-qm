#!/usr/bin/env python
# coding: utf-8

import numpy as np
import plotly.graph_objects as go

from scipy.constants import physical_constants, angstrom
BOHR_RADIUS = physical_constants["Bohr radius"][0] / angstrom


""" This module implements a class that compute the radial part of the
atomic orbitals of the hydrogen atom. """

__author__ = "Germain Salvato Vallverdu"
__email__ = "germain.vallverdu@univ-pau.fr"

radial_part_equations = r"""$$\begin{aligned}
    R_{10}(r) & = 2 \left(\frac{Z}{a_o}\right)^{3/2} \exp\left(-\frac{Zr}{a_o}\right) \\
    R_{20}(r) & = \frac{1}{2\sqrt{2}} \left(\frac{Z}{a_o}\right)^{3/2}  \left(2 - \frac{Zr}{a_o}\right) \exp\left(-\frac{Zr}{2a_o}\right) \\
    R_{21}(r) & = \frac{1}{2\sqrt{6}} \left(\frac{Z}{a_o}\right)^{5/2}  r \exp\left(-\frac{Zr}{2a_o}\right) \\
    R_{30}(r) & = \frac{2}{81\sqrt{3}} \left(\frac{Z}{a_o}\right)^{3/2} \left(27 - \frac{18Zr}{a_o} + \frac{2Z^2r^2}{{a_o}^2}\right) \exp\left(-\frac{Zr}{3a_o}\right) \\
    R_{31}(r) & = \frac{4}{81\sqrt{6}} \left(\frac{Z}{a_o}\right)^{5/2} \left(6r - \frac{Zr^2}{a_o}\right) \exp\left(-\frac{Zr}{3a_o}\right) \\
    R_{32}(r) & = \frac{4}{81\sqrt{30}} \left(\frac{Z}{a_o}\right)^{7/2}  r^2 \exp\left(-\frac{Zr}{3a_o}\right)
\end{aligned}$$"""


class AORadialPart:
    """ This class provides the radial parts of the atomic orbitals from
    1s to 3d. All functions are available as static methods. The radius
    r is in angstrom."""

    n_max = 4

    def __init__(self, n=1, l=0, Z=1):
        """ Select an atomic orbital depending on n et l quantum numbers

        Args:
            n (int): principal quantum number
            l (int): secondary quantum number
            Z (int): atomic number
        """
        try:
            self.n = int(n)
        except ValueError as e:
            print(e)
            raise ValueError(f"n must be an integer. n = {n}.")
        if not 0 < n <= self.n_max:
            raise ValueError(f"n must be lower or equal to 3. n = {n}.")

        try:
            self.l = int(l)
        except ValueError as e:
            print(e)
            raise ValueError(f"l must be an integer. l = {l}.")
        if not 0 <= l < self.n:
            raise ValueError(f"l must be in [0, {self.n - 1}]. l = {l}.")

        # select radial function
        self._radial = self._select_function()

    def _select_function(self):
        """ select the radial AO radial part depending on the n and l values """
        if self.n == 1 and self.l == 0:
            return self.radial1s
        elif self.n == 2:
            if self.l == 0:
                return self.radial2s
            elif self.l == 1:
                return self.radial2p
        elif self.n == 3:
            if self.l == 0:
                return self.radial3s
            elif self.l == 1:
                return self.radial3p
            elif self.l == 2:
                return self.radial3d
        elif self.n == 4:
            return self.radial4f

    def __call__(self, r, Z=1, ao=BOHR_RADIUS):
        """ compute the AO radial part """
        return self._radial(r, Z, ao)

    def get_plot(self, r_max=15, npts=400, Z=1, ao=BOHR_RADIUS):
        """ Return a plotly plot of the radial density and the wavefunction """

        r = np.linspace(0, r_max, npts)
        wf = self._radial(r, Z, ao)

        fig = go.Figure()

        # plot wavefunction
        fig.add_trace(
            go.Scatter(
                x=r,
                y=wf,
                mode="lines",
                name="wavefunction",
                line=dict(color="#1f77b4"),
            )
        )

        # plot probability density
        fig.add_trace(
            go.Scatter(
                x=r,
                y=r ** 2 * wf ** 2,
                mode="lines",
                name="D(r)",
                line=dict(color="#ff7f0e"),
                xaxis="x2"
            )
        )

        tickvals = [i * BOHR_RADIUS for i in range(1, 29, 3)]
        fig.update_layout(
            title=f"Radial probability density: n = {self.n}, l = {self.l}",
            height=600,  # width=600,
            xaxis=dict(
                range=[0, r_max], title="r (A)", gridcolor="LightGray",
                showline=True, linecolor="gray", ticks="inside",
                tickmode="array", tickvals=tickvals, tickangle=0,
                ticktext=[f"{i * BOHR_RADIUS:.1f}" for i in range(1, 29, 3)],
                zeroline=False
            ),
            yaxis=dict(
                range=[-.3, 1.05], gridcolor="LightGray", mirror=True,
                ticks="inside", linecolor="gray", showline=True,
                zeroline=True, zerolinecolor="LightGray", zerolinewidth=2
            ),
            xaxis2=dict(
                range=[0, r_max], title_text="r (ua)", showgrid=False,
                side="top", anchor="x", overlaying="x", title=dict(standoff=0),
                showline=True, linecolor="gray", ticks="inside",
                tickmode="array", tickvals=tickvals, tickangle=0,
                ticktext=[f"{i}ao" for i in range(1, 29, 3)],
            ),
            plot_bgcolor="white",
            # paper_bgcolor="white",
            legend=dict(
                xanchor="right", yanchor="top",
                x=0.95, y=0.95,
                bordercolor="LightGray", borderwidth=1,
            )
        )

        return fig

    @staticmethod
    def radial1s(r, Z=1, ao=BOHR_RADIUS):
        rho = Z * r / ao
        return 2 * np.sqrt(Z / ao)**3 * np.exp(- rho)

    @staticmethod
    def radial2s(r, Z=1, ao=BOHR_RADIUS):
        rho = Z * r / ao
        return 1 / (2 * np.sqrt(2)) * (Z / ao)**(3/2) * (2 - rho) * np.exp(- rho / 2)

    @staticmethod
    def radial2p(r, Z=1, ao=BOHR_RADIUS):
        rho = Z * r / ao
        return 1 / (2 * np.sqrt(6)) * (Z/ao)**(3/2) * rho * np.exp(- rho / 2)

    @staticmethod
    def radial3s(r, Z=1, ao=BOHR_RADIUS):
        rho = Z * r / ao
        return 2 / (81 * np.sqrt(3)) * (Z/ao)**(3/2) * (27 - 18*rho + 2*rho**2) * np.exp(- rho / 3)

    @staticmethod
    def radial3p(r, Z=1, ao=BOHR_RADIUS):
        rho = Z * r / ao
        return 4 / (81 * np.sqrt(6)) * (Z/ao)**(3/2) * (6 * rho - rho**2) * np.exp(- rho / 3)

    @staticmethod
    def radial3d(r, Z=1, ao=BOHR_RADIUS):
        rho = Z * r / ao
        return 4 / (81 * np.sqrt(30)) * (Z/ao)**(3/2) * rho**2 * np.exp(- rho / 3)

    @staticmethod
    def radial4f(r, theta, phi, ao=0.529, Z=1):
        """ TODO: check this !!"""
        rho = Z * r / ao
        radial = 1 / (768 * np.sqrt(35)) * (Z/ao)**(3/2) * \
            rho**3 * np.exp(- rho / 4)

        return radial
