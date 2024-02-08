import dash
import os 
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine
from dash_bootstrap_templates import load_figure_template

load_figure_template(["cyborg", "darkly"])
from utils.db import printa
from dash import Dash, html, dcc
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

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

# fig2 = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group", template='darkly')


df = pd.read_sql_query("select sum(total_price) as total_price,branch_id,employee_id from transaction group by branch_id,employee_id", engine)
fig2 = px.bar(df, x="employee_id", y="total_price", color="branch_id", barmode="group", template='darkly')


df = pd.read_sql_query("select * from transaction", engine)
fig = px.scatter(df, x="tran_date", y="total_price", template='darkly')



layout = html.Div(
    [
        dcc.Markdown('# This will be the content of Page 1'+printa("a")),
        dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    dcc.Graph(
        id='example-graph',
        figure=fig2
    )
    ]
)