import dash
from dash import dcc, html

dash.register_page(__name__,path='/home2',name="Sales Prediction 📈 ")
c = dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            },
            
        }
    )
layout = html.Div(children=[
    html.H1(children='Dash Example', style={'textAlign': 'center', 'color': '#007bff'}),

    html.Div(children='''
        Dash: A web application framework for Python.
    ''', style={'textAlign': 'center', 'color': '#007bff'}),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),
    html.Div(children=[
        html.Div([
    
            html.Div(children=[
                html.H1('Dash CSS long answer' , className="textappear"),
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
                # html.Label('Checkboxes'),
                # dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
                #             ['Montréal', 'San Francisco']
                # ),

                # html.Br(),
                # html.Label('Text Input'),
                # dcc.Input(value='MTL', type='text'),

                # html.Br(),
                # html.Label('Slider'),
                # dcc.Slider(
                #     min=0,
                #     max=9,
                #     marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
                #     value=5,
                # ),
                c,
            ], style={
                    #   'padding': '10vw 30vw' , 
                      'flex': 1
                      ,'width': '25%'
                      ,'border-radius': '25px'
                      ,'background': '#73AD21'
                      ,'padding': '20px' 
                      ,'margin': '20px' 
                      
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
                       'flex': 3

                      ,'width': '25%'
                      }),
            html.Div(children=[
                html.H1('Dash '),
            ], style={
                  'flex': 1
                      ,'width': '25%'
                      })
        ], style={'display': 'flex', 'flexDirection': 'row'})
    ])

], style={'padding': '20px'
        #   , 'backgroundColor': '#f8f9fa'
          })