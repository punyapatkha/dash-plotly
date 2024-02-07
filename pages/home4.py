import dash
from dash import dcc, html

dash.register_page(__name__,path='/home4',name="Faurd Detection ⚠️ ")

layout = html.Div(
    [
        dcc.Markdown('# This will b22e the content of Page 2')
    ]
)