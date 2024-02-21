from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash
import dash_auth
import os 
from dotenv import load_dotenv
load_dotenv()

# blog for deploy
# https://community.plotly.com/t/migrating-from-heroku-how-to-use-render-to-deploy-a-python-dash-app-solution/68048

# example code for deploy
# https://github.com/thusharabandara/dash-app-render-deployment/blob/main/app.py



df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

valueENV = os.getenv("Token") 
if valueENV is None:
    value = 'Token not found'
else:
    value = valueENV

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


# loads the "darkly" template and sets it as the default
load_figure_template("darkly")


VALID_USERNAME_PASSWORD_PAIRS = {
    'mindover': 'data2024'
}

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css",'styles.css',dbc.themes.DARKLY ]


app = Dash(__name__, pages_folder='pages' , use_pages=True, 
           external_stylesheets=external_css
           )
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

server = app.server


app.layout = html.Div(
    [   
        # header
        html.Div(children=[    
            html.Img(src="https://static.wixstatic.com/media/44b0f0_07215d41afde492e982c744e99ff55eb~mv2.png",
                    style={ 'max-width': '16vw','max-height': '16vw','margin-left':10,'margin-top':10})
            ,html.Div("Retail Dashboard Prototype",style={'text-shadow': '0 0 5px #000000, 0 0 15px #000000'})
        ], style={'fontSize':20
        #   ,'margin-top':20
        , 'textAlign':'center'}),
        dcc.Location(id='url', refresh=False), 
        
        html.Div([
            # dcc.Link("•  "+page['name'], href=page['path'], className="btn btn-dark m-2 fs-5")
            # for page in dash.page_registry.values()
            dcc.Link("• Sales Summary ", href='/', className="btn btn-dark m-2 fs-5"),
            dcc.Link("• Chat Mind Over Data 💬 ", href="/LLM", className="btn btn-dark m-2 fs-5"),
            dcc.Link("• Sales Prediction 📈 ", href="/", className="btn btn-dark m-2 fs-5 disabled"),
            dcc.Link("• Cluster Analysis 📊 ", href="/", className="btn btn-dark m-2 fs-5 disabled"),
            dcc.Link("• Faurd Detection ⚠️ ", href="/", className="btn btn-dark m-2 fs-5 disabled")
            
        ]
        , style={'fontSize':50, 'textAlign':'center'}
        ),
        html.Hr(),

        # content of each page
        # html.Div(dash.page_container,style={ 'min-height': '30vw'}),
        dash.page_container,
        # footer
        
        html.Hr(),
        
        html.Div("CONTACTS", style={'fontSize':15, 'textAlign':'center'}),
        html.Div("Reach out via email - mockup@mindoverdata.com.", style={'fontSize':12, 'textAlign':'center'}),
        html.Div("Don't miss any news - follow us at LinkedIn.", style={'fontSize':12, 'textAlign':'center'}),
        
        html.Div(id='url-output', style={'fontSize':10, 'textAlign':'center','padding-bottom':8}),
        # html.Hr()
    ]
)



@app.callback(
    Output('url-output', 'children'),
    [Input('url', 'pathname')]
)
def display_page_pathname(pathname):
    return f"The current URL is: {pathname}"

if __name__ == '__main__':

    # https://stackoverflow.com/questions/62378947/hot-reload-in-dash-does-not-automatically-update
    # around 2 sec after save

    app.run(debug=True)
    # what diff? run & run_server
    # app.run_server(debug=True)