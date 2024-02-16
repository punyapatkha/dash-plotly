import dash
import os 
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine
from dash_bootstrap_templates import load_figure_template

import dash_bootstrap_components as dbc
load_figure_template(["cyborg", "darkly"])
from utils.db import printa
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

valueENV = os.getenv("DBconnection") 
if valueENV is None:
    value = 'DB not found'
else:
    engine = create_engine(valueENV)
    df = pd.read_sql_query("select * from customer", engine)
    
    # with engine.connect() as conn:
    #     result = conn.execute("SELECT * FROM foo;")
    #     df = pd.DataFrame(result.all(), columns=result.keys())
    value = valueENV



dash.register_page(__name__,path='/',name="Sales Summary 📋 ")

# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig2 = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group", template='darkly')


df = pd.read_sql_query("select sum(total_price) as total_price,branch_id,employee_id from transaction group by branch_id,employee_id", engine)
fig2 = px.bar(df, x="employee_id", y="total_price", color="branch_id", barmode="group", template='darkly')


df = pd.read_sql_query("select * from transaction", engine)
fig = px.scatter(df, x="tran_date", y="total_price", template='darkly')


layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    # dcc.Slider(
    #     df['year'].min(),
    #     df['year'].max(),
    #     step=None,
    #     value=df['year'].min(),
    #     marks={str(year): str(year) for year in df['year'].unique()},
    #     id='year-slider'
    # ),
    # dcc.Dropdown(df['branch_id'].unique(), df['branch_id'].unique()[1],id='year-slider')
    dcc.Checklist(
    df['branch_id'].unique(),df['branch_id'].unique(),id='year-slider'
)
]),

@callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    # filtered_df = df[df.branch_id == selected_year]
    
    filtered_df = df[df.branch_id.isin(selected_year)]
    fig = px.scatter(filtered_df, 
                     y="total_price", 
                     x="branch_id",
                    #  size="pop", 
                    #  color="continent", 
                    #  hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

# layout =html.Div([
    
#     html.Div(children=[
#         html.Label('Dropdown'),
#         dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),

#         html.Br(),
#         html.Label('Multi-Select Dropdown'),
#         dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
#                      ['Montréal', 'San Francisco'],
#                      multi=True),

#         html.Br(),
#         html.Label('Radio Items'),
#         dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),
#     ], style={'padding': 30, 'flex': 1}),

#     html.Div(children=[
#         html.Label('Checkboxes'),
#         dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
#                       ['Montréal', 'San Francisco']
#         ),

#         html.Br(),
#         html.Label('Text Input'),
#         dcc.Input(value='MTL', type='text'),

#         html.Br(),
#         html.Label('Slider'),
#         dcc.Slider(
#             min=0,
#             max=9,
#             marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
#             value=5,
#         ),
#     ], style={'padding': '10vw 30vw' , 'flex': 1})
# ], style={'display': 'flex', 'flexDirection': 'row'})
