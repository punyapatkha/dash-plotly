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



#############################################################################
# total sale
#############################################################################

df_total_sale = pd.read_sql_query("""select * from (
select sum(total_price) as sale ,'today' as period from transaction
where tran_date = (select max(tran_date) from transaction)
union 
select sum(total_price) as sale,'this_month' as period from transaction
where (extract(month from tran_date) = (select extract(month from max(tran_date)) from transaction))
        and  
     (extract(year from tran_date) = (select extract(year from max(tran_date)) from transaction))
union 
select sum(total_price) as sale,'last_3month' as period from transaction
where tran_date > (select (max(tran_date)  -INTERVAL '3 MONTHS') from transaction)
union 
select sum(total_price) as sale,'last_12month' as period from transaction
where tran_date > (select (max(tran_date)  -INTERVAL '12 MONTHS') from transaction)
) subquery
order by sale """, engine)

# df_total_sale[df_total_sale["period"] == 'today']['sale'].iloc[0]
# df_total_sale[df_total_sale["period"] == 'this_month']['sale'].iloc[0]
# df_total_sale[df_total_sale["period"] == 'last_3month']['sale'].iloc[0]
# df_total_sale[df_total_sale["period"] == 'last_12month']['sale'].iloc[0]
#############################################################################
# line graph
#############################################################################

df_line = pd.read_sql_query("""
select sum(total_price) as sum_total_price ,branch_name,tran_date from 
(
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
-- c.id,
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
 where a.tran_date > (select ( max(tran_date)-INTERVAL '2 MONTHS') from transaction )
order by a.id asc


-- select * from "order"
) a
group by branch_name,tran_date 
order by tran_date
""",engine)

fig =  px.line(df_line, x="tran_date", y="sum_total_price", color="branch_name")
line_graph = dcc.Graph(figure=fig)
#############################################################################
# bar graph
#############################################################################

df_line = pd.read_sql_query("""
select count(*) as count,branch_name,tran_date from 
(
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
-- c.id,
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
 where a.tran_date > (select ( max(tran_date)-INTERVAL '2 MONTHS') from transaction )
order by a.id asc


-- select * from "order"
) a
group by branch_name,tran_date 
order by tran_date
""",engine)

fig =  px.line(df_line, x="tran_date", y="count", color="branch_name")
count_graph = dcc.Graph(figure=fig)
# fig =  px.bar(df_bar, x="tran_date", y="sum_total_price", color="branch_name")
# bar_graph = dcc.Graph(figure=fig)

#############################################################################
# pie chart
#############################################################################

df_pie = pd.read_sql_query("""select sum(total_price) as total_price,c.name as branch_name,employee_id from transaction a
                           left join branch c on a.branch_id = c.id
                           group by c.name,a.employee_id""", engine)
# fig = px.pie(df, values='total_price', names='employee_id')
# fig.show()

fig = px.pie(df_pie, values='total_price', names='branch_name')
pie_chart_total = dcc.Graph(figure=fig)
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
    Output('scatter-graph', 'figure'),
    Input('branch-checklist', 'value'))
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
                html.H4('Total Sale Today' , style={'margin':'2vw'} ),
                
                html.H3( str(df_total_sale[df_total_sale["period"] == 'today']['sale'].iloc[0])+" $"
 , style={'margin':'2vw','text-shadow': '0 0 5px #008000, 0 0 8px #2AAA8A'} ),
            ], style={
                        # 'padding': 30,
                       'flex': 1 
                      ,'width': '25%'
                      ,'border-radius': '10px'
                      ,'margin-left':'2vw'
                      ,'margin-right':'2vw'
                      ,'box-shadow': 'rgba(0, 0, 0, 0.35) 0px 5px 15px'
                      ,'background': '#0C0404'
                    #   , 'backgroundColor': '#f8f9fa'
                      }),
            html.Div(children=[
                html.H4('Total Sale This Month' , style={'margin':'2vw'}),
                html.H3(str(df_total_sale[df_total_sale["period"] == 'this_month']['sale'].iloc[0])+" $" , style={'margin':'2vw','text-shadow': '0 0 5px #008000, 0 0 8px #2AAA8A'} ),
            ], style={
                # 'padding': 30,
                  'flex': 1
                      ,'width': '25%'
                      ,'border-radius': '10px'
                      ,'margin-left':'2vw'
                      ,'margin-right':'2vw'
                      ,'box-shadow': 'rgba(0, 0, 0, 0.35) 0px 5px 15px'
                      ,'background': '#0C0404'
                    #   , 'backgroundColor': '#f8f9fa'
                      }),
            html.Div(children=[
                html.H4('Total Sale Last 3 Month', style={'margin':'2vw'} ),
                html.H3(str(df_total_sale[df_total_sale["period"] == 'last_3month']['sale'].iloc[0])+" $" , style={'margin':'2vw','text-shadow': '0 0 5px #008000, 0 0 8px #2AAA8A'} ),
            ], style={
                # 'padding': 30,
                  'flex': 1
                      ,'width': '25%'
                      ,'border-radius': '10px'
                      ,'margin-left':'2vw'
                      ,'margin-right':'2vw'
                      ,'box-shadow': 'rgba(0, 0, 0, 0.35) 0px 5px 15px'
                      ,'background': '#0C0404'
                    #   , 'backgroundColor': '#f8f9fa'
                      }),


            html.Div(children=[            
                html.H4('Total Sale Last 12 Month' , style={'margin':'2vw'} ),
                html.H3(  str(df_total_sale[df_total_sale["period"] == 'last_12month']['sale'].iloc[0])+" $" , style={'margin':'2vw','text-shadow': '0 0 5px #008000, 0 0 8px #2AAA8A'} ),
            ], style={
                    #   'padding': '10vw 30vw' , 
                      'flex': 1
                      ,'width': '25%'
                      ,'border-radius': '10px'
                      ,'background': '#0C0404'
                      
                      ,'margin-left':'2vw'
                      ,'margin-right':'2vw'
                      ,'box-shadow': 'rgba(0, 0, 0, 0.35) 0px 5px 15px'
                    #   ,'border-radius': '20px'
                    #   ,'background': '#73AD21'
                    #   ,'box-shadow': 'rgba(0, 0, 0, 0.35) 0px 5px 15px'
                    #   ,'padding': '20px' 
                    #   ,'margin': '20px' 
                      
                      })
        ], style={'display': 'flex', 'flexDirection': 'row' , 'margin-bottom':'2vw' , 'margin-top':'2vw'
                  })
    ]),


    html.Div(children=[
        html.Div([
    
            html.Div(children=[
                count_graph
            ], style={
                       'flex': 1 
                      ,'width': '25%'
                      ,'margin-left':'2vw'
                      ,'margin-right':'2vw'
                      ,'box-shadow': 'rgba(0, 0, 0, 0.35) 0px 5px 15px'
                      }),
            # html.Div(children=[
            #     # html.H1('Dash '),
            #     # line_graph
            #     pie_chart_total
            # ], style={
            #       'flex': 1
            #           ,'width': '25%'
                      
            #           ,'padding-right':'2vw'
            #           ,'box-shadow': 'rgba(0, 0, 0, 0.35) 0px 5px 15px'
            #           })
        ], style={'display': 'flex', 'flexDirection': 'row'})
    ]),

    html.Div(children=[
        html.Div([
    
            html.Div(children=[
                pie_chart_total,
                # line_graph
                
            ], style={
                       'flex': 1
                      ,'width': '25%'
                      ,'background': '#0C0404'
                      ,'margin': '2vw'
                      ,'border-radius': '20px'
                      ,'box-shadow': 'rgba(0, 0, 0, 0.35) 0px 5px 15px'
                      }),
            html.Div(children=[
                
                    dcc.Graph(id='scatter-graph'),
                    html.Div('Transaction from Branch',style={'padding-left':'8px',
                                                              'padding-top':'8px'}),
                    dcc.Checklist(
                    df['branch_name'].unique(),df['branch_name'].unique(),id='branch-checklist'
                    ,labelStyle={"display": "row","padding":"10px"}
                    # ,labelStyle={"display": "flex","padding":"8px"}
                    ,inputStyle={"padding":"8px","margin-right":"8px"})
            ], style={
                  'flex': 1
                    #   ,'width': '25vw'
                      ,'margin': '2vw'
                      
                      ,'border-radius': '20px'
                    #   ,'background': '#333333'
                      ,'background': '#0C0404'
                      ,'box-shadow': 'rgba(0, 0, 0, 0.35) 0px 5px 15px'
                    
                      })
        ], style={'display': 'flex', 'flexDirection': 'row'})
    ]) 
] , className="textappear")
