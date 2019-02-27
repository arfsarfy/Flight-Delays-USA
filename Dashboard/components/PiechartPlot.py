import numpy as np
estm ={
    'Count':len,
    'Average':np.mean,
    'Sum':sum,
    'Standard Deviation':np.std
}
col_y = {'Airline':'ABBR_AIRLINE',
        'Departure Month':'SD_MONTH',
        }
col_x = {'Distance':'DISTANCE',
        'Departure Delay':'DEPARTURE_DELAY',
        'Arrival Delay':'ARRIVAL_DELAY',
        'Air Time':'AIR_TIME',
        'Delay in Minute':'TOTAL_DELAY_MIN',
        'Delay':'DELAY'
        }

def renderpie(df,html,dcc):
    return html.Div([                                                          
                html.H1('Pie Chart',className='h1_x'),
                html.Div(className='row justify-content-md-center', children=[
                    html.Div(className='col-4',children=[
                        html.P('Hue :',className='text_modified'),
                        dcc.Dropdown(
                                id='PC_Hue',
                                options=[{'label': i, 'value': col_y[i]} for i in ['Airline','Departure Month']],
                                value='ABBR_AIRLINE',
                                # style={'width':'300px'}
                                    )
                            ],
                    # style={'margin':'0 auto'}
                    ),
                    html.Div(className='col-4',children=[
                        html.P('Estimator :',className='text_modified'),
                        dcc.Dropdown(
                                id='PC_Estimator',
                                options=[{'label': i, 'value': i} for i in list(estm.keys())],
                                value='Count',
                                # style={'width':'300px'}
                                    )
                            ],
                    # style={'margin':'0 auto'}
                    ),html.Div(className='col-4',children=[
                        html.P('Data :',),
                        dcc.Dropdown(
                                id='PC_Data',
                                options=[{'label': i, 'value':  col_x[i]} for i in col_x.keys()],
                                value='TOTAL_DELAY_MIN',
                                # style={'width':'300px'}
                                    )
                            ],
                    # style={'margin':'0 auto'}
                    )
                    ]),
                html.Br(),
                dcc.Graph(id='PieChart')                                                                                                              
                    ])
                