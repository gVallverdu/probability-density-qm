# coding: utf-8

from dash import html


def footer(logo_img, logo_url):
    return html.Div(className="footer", children=[
        html.Div(className="row", children=[
            html.Div(className="six columns", children=[
                html.A(
                    html.Img(
                        src=logo_img,
                        # src="http://gvallver.perso.univ-pau.fr/img/logo_uppa.png",
                        height="50px",
                    ),
                    # href="https://www.univ-pau.fr"
                    href=logo_url,
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
    ])
