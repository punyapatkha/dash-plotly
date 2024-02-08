import dash
from dash import dcc, html
import os 
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine
import pandas as pd
from utils.db import printa

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

layout = html.Div(
    [
        dcc.Markdown('# This will be the content of Page 1'+printa("a"))
    ]
)