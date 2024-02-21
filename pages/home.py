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



df = pd.read_sql_query("select sum(total_price) as total_price,branch_id,employee_id from transaction group by branch_id,employee_id", engine)
fig2 = px.bar(df, x="employee_id", y="total_price", color="branch_id", barmode="group", template='darkly')

#############################################################################
# scatter graph
#############################################################################


df = pd.read_sql_query("""
select 
a.id,
a.total_price,
-- a.employee_id,
-- a.cust_id,
date(a.tran_date) as tran_date,
-- b.id,
b.price,
b.amount,
b.amount_price as order_price,
b.product_id,
b.tran_id,
c.id as branch_id,
c.name as branch_name,
c.address_province as branch_address,
-- d.id,
d.name as product_cat,
-- e.id,
e.name as product_name,
e.unit_price,
e.cat_id

-- c.*,extract(month from a.tran_date) "tran_month" ,extract(year from a.tran_date) as "tran_year"
-- ,b.*
-- ,b.amount,b.price,b.amount_price,b.product_id,b.tran_id
from transaction a 
left join "order" b on a.id = b.tran_id
left join branch c on a.branch_id = c.id
left join categories d on b.product_id = d.id
left join product e on b.product_id = e.id
-- where 
order by a.id asc
""", engine)
fig = px.scatter(df, x="tran_date", y="total_price", template='darkly')



@callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_branch):
    # filtered_df = df[df.branch_name == selected_branch]
    
    filtered_df = df[df.branch_name.isin(selected_branch)]
    fig = px.scatter(filtered_df, 
                     y="total_price", 
                     x="tran_date",
                    #  size="pop", 
                     color="branch_name", 
                    #  hover_name="country",
                    #  log_x=True,
                       size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

#############################################################################
#
#############################################################################

layout = html.Div([

   
       html.Div(children=[
        html.Div([
    
            html.Div(children=[
                html.H1('Dash' , className="textappear"),
            ], style={
                        # 'padding': 30,
                       'flex': 1 
                      ,'width': '25%'
                    #   , 'backgroundColor': '#f8f9fa'
                      }),
            html.Div(children=[
                html.H1('Dash '),
            ], style={
                # 'padding': 30,
                  'flex': 1
                      ,'width': '25%'
                    #   , 'backgroundColor': '#f8f9fa'
                      }),
            html.Div(children=[
                html.H1('Dash '),
            ], style={
                # 'padding': 30,
                  'flex': 1
                      ,'width': '25%'
                    #   , 'backgroundColor': '#f8f9fa'
                      }),


            html.Div(children=[            
                html.H1('  Dash ', style={
                      'border-radius': '20px'
                      ,'background': '#73AD21'
                      ,'box-shadow': 'rgba(0, 0, 0, 0.35) 0px 5px 15px'
                      ,'width': '80%'
                        # ,'padding': '20px' 
                    #   ,'margin': '20px' 
                })
            ], style={
                    #   'padding': '10vw 30vw' , 
                      'flex': 1
                      ,'width': '25%'
                    #   ,'border-radius': '20px'
                    #   ,'background': '#73AD21'
                    #   ,'box-shadow': 'rgba(0, 0, 0, 0.35) 0px 5px 15px'
                    #   ,'padding': '20px' 
                    #   ,'margin': '20px' 
                      
                      })
        ], style={'display': 'flex', 'flexDirection': 'row'})
    ]),


    html.Div(children=[
        html.Div([
    
            html.Div(children=[
                html.H1('Dash '),
            ], style={
                       'flex': 1 
                      ,'width': '25%'
                      }),
            html.Div(children=[
                html.H1('Dash '),
            ], style={
                  'flex': 1
                      ,'width': '25%'
                      })
        ], style={'display': 'flex', 'flexDirection': 'row'})
    ]),

    html.Div(children=[
        html.Div([
    
            html.Div(children=[
                html.H1('Dash '),
                
            ], style={
                       'flex': 1

                      ,'width': '25%'
                      }),
            html.Div(children=[
                
                    dcc.Graph(id='graph-with-slider'),
                    html.Div('Transaction from Branch',style={'padding-left':'8px',
                                                              'padding-top':'8px'}),
                    dcc.Checklist(
                    df['branch_name'].unique(),df['branch_name'].unique(),id='year-slider'
                    ,labelStyle={"display": "row","padding":"10px"}
                    # ,labelStyle={"display": "flex","padding":"8px"}
                    ,inputStyle={"padding":"8px","margin-right":"8px"})
            ], style={
                  'flex': 3
                      ,'width': '25vw'
                      ,'margin': '2vw'
                      
                      ,'border-radius': '20px'
                      ,'background': '#333333'
                      ,'box-shadow': 'rgba(0, 0, 0, 0.35) 0px 5px 15px'
                    
                      })
        ], style={'display': 'flex', 'flexDirection': 'row'})
    ]) 
])
