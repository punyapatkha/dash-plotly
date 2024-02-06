from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash

import os 
from dotenv import load_dotenv
load_dotenv()

# blog for deploy
# https://community.plotly.com/t/migrating-from-heroku-how-to-use-render-to-deploy-a-python-dash-app-solution/68048

# example code for deploy
# https://github.com/thusharabandara/dash-app-render-deployment/blob/main/app.py



df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css",'styles.css' ]

valueENV = os.getenv("Token") 
if valueENV is None:
    value = 'Token not found'
else:
    value = valueENV

app = Dash(__name__, pages_folder='pages' , use_pages=True, external_stylesheets=external_css)
server = app.server


app.layout = html.Div(
    [
        # main app framework
        html.Div("Python Multipage App with Dash"+value, style={'fontSize':50, 'textAlign':'center'}),
        html.Div([
            dcc.Link("•  "+page['name'], href=page['path'], className="btn btn-dark m-2 fs-5")
            for page in dash.page_registry.values()
        ]
        , style={'fontSize':50, 'textAlign':'center'}
        ),
        html.Div([
            dcc.Link("•  "+page['name'], href=page['path'], style={'background-color':'#555555','fontSize':30,
                                                                   'color':'white','margin': '10px',
                                                                   'border-radius': '3px'})
            for page in dash.page_registry.values()
        ]
        , style={'fontSize':50, 'textAlign':'center'}
        ),
        html.Hr(),

        # content of each page
        dash.page_container
    ]
)

# app.layout = html.Div([
#     html.H1('Multi-page app with Dash Pages'),
#     html.Div([
#         html.Div(
#             dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
#         ) for page in dash.page_registry.values()
#     ]),
#     dash.page_container
# ])


if __name__ == '__main__':

    # https://stackoverflow.com/questions/62378947/hot-reload-in-dash-does-not-automatically-update
    # around 2 sec after save

    app.run(debug=True)
    # what diff? run & run_server
    # app.run_server(debug=True)