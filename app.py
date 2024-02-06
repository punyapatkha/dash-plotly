from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash
# blog for deploy
# https://community.plotly.com/t/migrating-from-heroku-how-to-use-render-to-deploy-a-python-dash-app-solution/68048

# example code for deploy
# https://github.com/thusharabandara/dash-app-render-deployment/blob/main/app.py



df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__, pages_folder='pages' , use_pages=True)
# server = app.server


app.layout = html.Div(
    [
        # main app framework
        html.Div("Python Multipage App with Dash", style={'fontSize':50, 'textAlign':'center'}),
        html.Div([
            dcc.Link(page['name']+"  |  ", href=page['path'])
            for page in dash.page_registry.values()
        ]),
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