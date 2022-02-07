# coding: utf-8

from dash import html


def header(title, url, fa_icon=""):
    """ Returns the header layout with a github link icon. 

    Args:
        title (str): the title page
        url (str): the url of the github repo
    """

    return html.Div(className="header", children=[
        html.Div(id="github-div", children=[
            html.A(
                id="github-link",
                href=url,
                children=[
                    html.Span(
                        id="github-icon", className="fab fa-github fa-2x",
                        style={"verticalAlign": "bottom"}),
                    " View on GitHub"])
        ]),
        html.H1([html.I(className=fa_icon), " ", title]),
    ])
