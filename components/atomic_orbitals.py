#!/usr/bin/env python
# coding: utf-8

import numpy as np
import plotly.graph_objects as go

from scipy.constants import physical_constants, angstrom
BOHR_RADIUS = physical_constants["Bohr radius"][0] / angstrom


""" This module implements wave functions to be considered in the
application. """

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

angular_part_equation = r"""$$\begin{aligned}
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
        if 0 < n <= self.n_max:
            try:
                self.n = int(n)
            except ValueError as e:
                print(e)
                raise ValueError(f"n must be an integer. n = {n}.")
        else:
            raise ValueError(f"n must be lower or equal to 3. n = {n}.")

        if 0 <= l < self.n:
            try:
                self.l = int(l)
            except ValueError as e:
                print(e)
                raise ValueError(f"l must be an integer. l = {l}.")
        else:
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


class AOAngularPart:
    r""" This class provides the angular parts of the atomic orbitals as
    spherical harmonic. All functions are available as static methods. 

    Only real functions are considered. Real functions can be obtained 
    from the linear combination of spherical harmonic with the same value
    of l and the same absolute value of m_l. For example:

    $$
        \frac{1}{\sqrt 2} \left(-Y_1^1 + Y_1^{-1}\right) = \sqrt{\frac{3}{2\pi}} \sin\theta\cos\varphi
    $$
    """

    def __init__(self, l=0, m_l=0):
        """ Select an atomic orbital depending on l and m_l quantum numbers

        Args:
            l (int): secondary quantum number
            m_l (int): magnetic quantum number
        """
        if 0 <= l <= 3:
            try:
                self.l = int(l)
            except ValueError as e:
                print(e)
                raise ValueError(f"l must be an integer. l = {l}.")
        else:
            raise ValueError(f"l must be in [0, 3]. l = {l}.")

        if 0 <= l < self.n:
            try:
                self.l = int(l)
            except ValueError as e:
                print(e)
                raise ValueError(f"l must be an integer. l = {l}.")
        else:
            raise ValueError(f"l must be in [0, {self.n - 1}]. l = {l}.")

    @staticmethod
    def Y00(theta, phi):
        return 1 / np.sqrt(4 * np.pi)

    @staticmethod
    def Y10(theta, phi):
        return np.sqrt(3 / (4 * np.pi)) * np.cos(theta)

    @staticmethod
    def Y20(theta, phi):
        return np.sqrt(5 / (16 * np.pi)) * (3 * np.cos(theta)**2 - 1)

    @staticmethod
    def Y30(theta, phi):
        return np.sqrt(7 / (16 * np.pi)) * (5 * np.cos(theta)**3 - 3 * np.cos(theta))

    @staticmethod
    def Y11x(theta, phi):
        """ 1 / sqrt(2) (-Y_1^1 + Y_1^-1) """
        return np.sqrt(3 / (4 * np.pi)) * np.sin(theta) * np.cos(phi)

    @staticmethod
    def Y21xz(theta, phi):
        """ 1 / sqrt(2) (-Y_2^1 + Y_2^-1) """
        return np.sqrt(15 / (2 * np.pi)) * np.sin(theta) * np.cos(theta) * np.cos(phi)

    @staticmethod
    def Y31xz2(theta, phi):
        """ 1 / sqrt(2) (-Y_3^1 + Y_3^-1) """
        return np.sqrt(21 / (32 * np.pi)) * np.sin(theta) * (5 * np.cos(theta)**2 - 1) * np.cos(phi)


def pos_neg_part(fonction, theta, phi=0):
    """ return the positive and negative part of the fonction """
    r = fonction(theta, phi)
    ix = np.where(r >= 0)
    xp = r[ix] * np.sin(theta[ix])
    zp = r[ix] * np.cos(theta[ix])
    ix = np.where(r < 0)
    xn = -r[ix] * np.sin(theta[ix])
    zn = -r[ix] * np.cos(theta[ix])
    return xp, zp, xn, zn


# ## 3. Orbitales atomiques
#
# L'expression générale des orbitales atomiques fait intervenir une partie
# radiale et une partie angulaire et est caractérisée par les trois nombres
# quantiques $(n, \ell, m_{\ell})$ :
# \begin{equation*}
# \Psi_{n, \ell, m_{\ell}}(r, \theta, \varphi) = R_{n, \ell} (r) \, Y_{\ell}^{m_{\ell}}(\theta, \varphi)
# \end{equation*}
#
# On représente la densité électronique associée à différentes orbitales atomiques dans le plan $(xOz)$.

def sample(fonction, rmax=10, ntry=10000, phi=0):
    """ échantillonage de la densité de probabilité de présence associée à une OA """
    x = np.random.uniform(-rmax, rmax, ntry)
    z = np.random.uniform(-rmax, rmax, ntry)
    r = np.sqrt(x**2 + z**2)
    theta = np.arccos(z / r)  # le theta des sphériques

    rho = fonction(r, theta, phi=phi)**2
    rnd = np.random.rand(ntry)
    ix = np.where(rho > rnd)
    return x[ix], z[ix]


# ### Orbitales atomiques de symétrie sphérique

def OA1s(r, theta, phi, ao=0.529, Z=1):
    return AORadialPart.radial1s(r, Z, ao) * AOAngularPart.Y00(theta, phi)


def OA2s(r, theta, phi, ao=0.529, Z=1):
    return AORadialPart.radial2s(r, Z, ao) * AOAngularPart.Y00(theta, phi)


def OA3s(r, theta, phi, ao=0.529, Z=1):
    return AORadialPart.radial3s(r, Z, ao) * AOAngularPart.Y00(theta, phi)


def OA2pz(r, theta, phi, ao=0.529, Z=1):
    return AORadialPart.radial2p(r, Z, ao) * AOAngularPart.Y10(theta, phi)


def OA3pz(r, theta, phi, ao=0.529, Z=1):
    return AORadialPart.radial3p(r, Z, ao) * AOAngularPart.Y10(theta, phi)


def OA3dz2(r, theta, phi, ao=0.529, Z=1):
    return AORadialPart.radial3d(r, Z, ao) * AOAngularPart.Y20(theta, phi)


def OA4fz3(r, theta, phi, ao=0.529, Z=1):
    rho = Z * r / ao
    radial = 1 / (768 * np.sqrt(35)) * (Z/ao)**(3/2) * \
        rho**3 * np.exp(- rho / 4)
    return radial * AOAngularPart.Y30(theta, phi)
