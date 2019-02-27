col_y = {'Airline':'ABBR_AIRLINE',
        'Departure Month':'SD_MONTH',
        }
col_x = {'Distance':'DISTANCE',
        'Departure Delay':'DEPARTURE_DELAY',
        'Arrival Delay':'ARRIVAL_DELAY',
        'Air Time':'AIR_TIME',
        'Delay in Minute':'TOTAL_DELAY_MIN',
        }

def getPlot(df,jenis,x_axis,y_axis,go):
    list_gofunc={
    'bar':go.Bar,
    'violin':go.Violin,
    'box':go.Box
            }
    if jenis == 'bar':
        return [list_gofunc[jenis](
                    x=df[df['DELAY']==0][x_axis],
                    y=df[df['DELAY']==0][y_axis],
                    # text='Type 1 :'+df['Type 1']+'\nType 2 :'+df['Type 2'],
                    opacity=0.7,
                    name='NOT DELAYED',
                    marker=dict(color='green'),
                    orientation = 'h'
                ),
                list_gofunc[jenis](
                    x=df[df['DELAY']==1][x_axis],
                    y=df[df['DELAY']==1][y_axis],
                    # text='Type 1 :'+df['Type 1']+'\nType 2 :'+df['Type 2'],
                    opacity=0.7,
                    name='DELAYED',
                    marker=dict(color='red'),
                    orientation = 'h'
                )
                ]
    else:
        return [list_gofunc[jenis](
                    y=df[x_axis],
                    x=df[y_axis],
                    # text='Type 1 :'+df['Type 1']+'\nType 2 :'+df['Type 2'],
                    opacity=0.7,
                    # name='NOT DELAYED',
                    marker=dict(color='orange'),
                )
                ]





def rendercatplot(df,html,dcc):
    return html.Div([                                                          
                html.H1('Category Plot',className='h1_x'),
                html.Div('Plot Type',className='text_modified'),
                html.Div(className='row justify-content-md-center', children=[
                    html.Div(className='col-6',children=[
                        dcc.Dropdown(
                                id='jenisPlot',
                                options=[{'label': i, 'value': i.lower()} for i in ['Bar','Box','Violin']],
                                value='bar',
                                # style={'width':'300px'}
                                    )
                            ],
                    # style={'margin':'0 auto'}
                    )
                    ]),
                html.Br(),
                html.Div(className='row justify-content-md-center', children=[
                    html.Div('Axis  1 ',className='col-md-auto'),
                    html.Div(className='col col-lg-2',children=[
                        dcc.Dropdown(
                                id='y_axis',
                                options=[{'label': i, 'value': col_y[i]} for i in ['Airline','Departure Month']],
                                value='ABBR_AIRLINE',
                                # style={'width':'300px'}
                                    )],
                    # style={'margin':'0 auto'}
                    ),
                    html.Div('Axis  2  ',className='col-md-auto'),
                    html.Div(className='col col-lg-2',children=[
                        dcc.Dropdown(
                                id='x_axis',
                                options=[{'label': i, 'value':  col_x[i]} for i in col_x.keys()],
                                value='TOTAL_DELAY_MIN',
                                # style={'width':'300px'}
                                    )],
                    # style={'margin':'0 auto'}
                    )

                    ]),
                dcc.Graph(id='CategoricalPlot', style={'overflowX': 'scroll', 'overflowY': 'scroll', 'height': 600})                                                                                                              
                    ])
                