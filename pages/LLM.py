import dash
from dash import dcc, html , Input, Output, callback,State
import plotly.express as px
import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
import time

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool



load_dotenv()

dash.register_page(__name__,path='/LLM',name="Chat Mind Over Data 💬")

df = px.data.tips()

layout = html.Div(
    [
        # dcc.RadioItems([x for x in df.day.unique()], id='day-choice'),
        # dcc.Graph(id='bar-fig',
        #           figure=px.bar(df, x='smoker', y='total_bill')),
        html.H1("Chat Bot Example"),
        dcc.Loading(

        html.Div(id="chat-container2", children=[html.H1("Place holder text before update_chat function is run")])
        # ,type="circle"
        ),
        html.Div([
        dcc.Input(id="user-input", type="text", placeholder="  Enter Your Question...   "
                  ,style={
                      'border': '2px solid #808080',
                      'border-radius': '4px',
                      'width' : '400px',
                      'margin':'20px',
                      'padding':'5px'
                      
                  }),
        html.Button(id="submit-button", n_clicks=0, children="Submit"),
        ], className="textappear" , style={'margin':'20px'}),
    ]
, className="textappear", style={'position': 'relative','max-width': '50vw','min-height': '25vw'} )

@callback(
    Output("chat-container2", "children"),
    [Input("submit-button", "n_clicks")],
    [State("user-input", "value")]
)
def update_chat(n_clicks, user_input):
    if n_clicks is not None and user_input is not None:
        try:
            DATABASE_URL=os.getenv("DBconnection") 
            db = SQLDatabase.from_uri(DATABASE_URL)
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            chain = create_sql_query_chain(llm, db)
            
            # first response
            # response = chain.invoke({"question": user_input})
            # # response is sql statement
            # # print(response)
            
            # # db_response is result of sql query
            # # print(db.run(response))
            # db_response = db.run(response)
            # chat_history = [
            #     html.Div([
            #         # html.Div("User: " + user_input, style={"color": "blue"}),
            #         # html.Div("Bot: " + "Hello! How can I assist you?"+user_input, style={"color": "red"}),
            #         html.Div("User: " + user_input, style={"color": "white"}),
            #         html.Div("Bot response: " + response , style={"color": "white"}),
            #         html.Div("Bot response: " + db_response , style={"color": "white"}),
            #     ])
            # ]

            execute_query = QuerySQLDataBaseTool(db=db)
            write_query = create_sql_query_chain(llm, db)

            answer_prompt = PromptTemplate.from_template(
                """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

            Question: {question}
            SQL Query: {query}
            SQL Result: {result}
            Answer: """
            )

            answer = answer_prompt | llm | StrOutputParser()
            chain = (
                RunnablePassthrough.assign(query=write_query).assign(
                    result=itemgetter("query") | execute_query
                )
                | answer
            )

            answer = chain.invoke({"question": user_input})
            chat_history = [
                html.Div([
                    html.Hr(),
                    html.Div("Question : " +user_input, style={"color": "white"}, className="appearanima"),
                    html.Hr(),
                    # html.Div( user_input, style={"color": "white"}),
                    html.Div("Bot Response: ", style={"color": "white"}, className="appearanima"),
                    # html.Hr(),
                    html.Div( answer , style={"color": "white" }, className="appearanima")
                ])
            ]
            return chat_history

        except:
            return [html.H1("unexpected error LLM")]
    else:
        return [html.H1("How can we help you today", className="textappear")]
    

