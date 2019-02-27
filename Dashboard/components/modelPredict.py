import dash_core_components as dcc
import dash_html_components as html
import numpy as np

def renderModelPredict(df) :
    return html.Div([
                html.H1('Check Flight Delay', className='h1'),
                html.Div(children=[
                    html.Div([
                        html.P('Origin : ')
                    ],className='col-2'),
                    html.Div([
                        dcc.Dropdown(
                                id='origin_airport',
                                options=[{'label': i, 'value': i} for i in np.sort(df.ORIGIN_AIRPORT.unique())],
                                # value='ABBR_AIRLINE',
                                # style={'width':'300px'}
                                    )
                    ],className='col-4'),
                    html.Div([
                        html.P('Destination: ')
                    ],className='col-2'),
                    html.Div([
                        dcc.Dropdown(
                                id='destination_airport',
                                options=[{'label': i, 'value': i} for i in np.sort(df.DESTINATION_AIRPORT.unique())],
                                # value='ABBR_AIRLINE',
                                # style={'width':'300px'}
                                    )
                    ],className='col-4'),
                    html.Div([
                        html.P('Distance : ')
                    ],className='col-2'),
                    html.Div('',id='distance',className='col-4'),
                    html.Div([
                        html.P('Airtime : ')
                    ],className='col-2'),
                    html.Div('',id='airtime',className='col-4'),
                    html.Div([
                        html.P('Departure Day: ')
                    ],className='col-2'),
                    html.Div([
                        dcc.Input(id='depart_day', type='number', value='0')
                    ],className='col-4'),
                    html.Div([
                        html.P('Departure Month: ')
                    ],className='col-2'),
                    html.Div([
                        dcc.Input(id='depart_month', type='number', value='0')
                    ],className='col-4'),
                    html.Div([
                        html.P('Departure Hour:')
                    ],className='col-2'),
                    html.Div([
                        dcc.Input(id='depart_hour', type='number', value='0')
                    ],className='col-4'),
                    html.Div([
                        html.P('Arrival Day: ')
                    ],className='col-2'),
                    html.Div([
                        dcc.Input(id='arr_day', type='number', value='0')
                    ],className='col-4'),
                    html.Div([
                        html.P('Arrival Month: ')
                    ],className='col-2'),
                    html.Div([
                        dcc.Input(id='arr_month', type='number', value='0')
                    ],className='col-4'),
                    html.Div([
                        html.P('Arrival Hour : ')
                    ],className='col-2'),
                    html.Div([
                        dcc.Input(id='arr_hour', type='number', value='0')
                    ],className='col-4'),html.Div([
                        html.P('Time Required ')
                    ],className='col-2'),
                    html.Div('',id='sched_time',className='col-4'),
                    
                    html.Div([
                        html.Button('Predict', id='buttonPredict', className='btn btn-primary')
                    ],className='mx-auto', style={ 'paddingTop': '20px', 'paddingBottom': '20px' })
                ],className='row'),
                html.Div([
                    html.H2('', id='outputPredict', className='mx-auto')
                ], className='row')
            ])