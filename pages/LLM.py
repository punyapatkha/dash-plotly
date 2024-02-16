import dash
from dash import dcc, html , Input, Output, callback,State
import plotly.express as px

dash.register_page(__name__,path='/LLM',name="Chat Mind Over Data 💬")

df = px.data.tips()

layout = html.Div(
    [
        # dcc.RadioItems([x for x in df.day.unique()], id='day-choice'),
        # dcc.Graph(id='bar-fig',
        #           figure=px.bar(df, x='smoker', y='total_bill')),
        html.H1("Chat Bot Example"),
        html.Div(id="chat-container2", children=[html.H1("Place holder text before update_chat function is run")]),
        html.Div([
        dcc.Input(id="user-input", type="text", placeholder="Enter your message..."),
        html.Button(id="submit-button", n_clicks=0, children="Submit"),
        ]),
    ]
)

@callback(
    Output("chat-container2", "children"),
    [Input("submit-button", "n_clicks")],
    [State("user-input", "value")]
)
def update_chat(n_clicks, user_input):
    if n_clicks is not None and user_input is not None:
        
        chat_history = [
            html.Div([
                html.Div("User: " + user_input, style={"color": "blue"}),
                html.Div("Bot: " + "Hello! How can I assist you?"+user_input, style={"color": "red"})
            ])
        ]
        return chat_history
    else:
        return [html.H1("How can i help you today")]