import dash
from dash import dcc, html

dash.register_page(__name__,path='/home2',name="Hello 👋 ")

layout = html.Div(
    [
        dcc.Markdown('# This will be the content of Page 2')
    ]
)