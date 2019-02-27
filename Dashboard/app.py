import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pickle
from components.Table import renderTable
from components.scatterPlot import renderScatterPlot
from components.modelPredict import renderModelPredict
from components.catPlot import rendercatplot,getPlot
from components.PiechartPlot import renderpie

loadModel = pickle.load(open('flight_rfc_model.sav', 'rb'))

estm ={
    'Count':len,
    'Average':np.mean,
    'Sum':sum,
    'Standard Deviation':np.std
}

app = dash.Dash(__name__)

server = app.server

df = pd.read_csv('../flights_sample_cleaned.csv')
df = df.sample(frac=0.10)

app.title = 'Flight Delay Dataset'

app.layout = html.Div(children=[
    html.H1(children='Dashboard Flight Delay',className='titleDashboard'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Flight Delay Data', value='tab-1',children=[
            renderTable(df)
        ]),
        dcc.Tab(label='Categorical Plot', value='tab-2',children=[
            rendercatplot(df,html,dcc)
        ]),
        dcc.Tab(label='Pie Chart', value='tab-3',children=[
            renderpie(df,html,dcc)
        ]),
        dcc.Tab(label='Predict Flight Ticket', value='tab-4',children=[
            renderModelPredict(df)
        ]),

    ], style={
        'fontFamily': 'system-ui'
    }, content_style={
        'fontFamily': 'Arial',
        'borderBottom': '1px solid #d6d6d6',
        'borderLeft': '1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'padding': '44px'
    })
], style={
    'maxWidth': '1200px',
    'margin': '0 auto'
})
# TAB 1
@app.callback(
    Output('table-multicol-sorting', "data"),
    [Input('table-multicol-sorting', "pagination_settings"),
     Input('table-multicol-sorting', "sorting_settings")])
def update_graph(pagination_settings, sorting_settings):
    # print(sorting_settings)
    if len(sorting_settings):
        dff = df.head(500).sort_values(
            [col['column_id'] for col in sorting_settings],
            ascending=[
                col['direction'] == 'asc'
                for col in sorting_settings
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = df.head(500)

    return dff.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('rows')

#TAB 2
@app.callback(
    Output(component_id='CategoricalPlot', component_property='figure'),
    [Input(component_id='jenisPlot', component_property='value'),
    Input(component_id='x_axis', component_property='value'),
    Input(component_id='y_axis', component_property='value')])

def update_graphcat(jenis_plot, x_axis,y_axis ):
    
    return {'data':getPlot(df,jenis_plot,x_axis,y_axis,go),
        'layout':go.Layout(
        xaxis=dict(title=x_axis),
        # yaxis=dict(title=y_axis),
        margin=dict(l=150,b=150,t=10,r=90),
        # legend={'x':0,'y':1},
        hovermode='closest',
        boxmode='group',violinmode='group'
            )
        }


#TAB 3
@app.callback(
    Output(component_id='PieChart', component_property='figure'),
    [Input(component_id='PC_Hue', component_property='value'),
     Input(component_id='PC_Estimator', component_property='value'),
     Input(component_id='PC_Data', component_property='value')])

def update_graphpie(hue, fn,data):
    return {'data':[
                    go.Pie(
                        labels=sorted(list(df[hue].unique())),
                        values=[estm[fn](df[df[hue] == item][data]) for item in sorted(list(df[hue].unique()))],
                        # textinfo='value',
                        hoverinfo='label+value',
                        # sort=False
                        )   
                    ],
            'layout':go.Layout(
                        margin=dict(l=40,b=40,t=10,r=10),
                        legend={'x':0,'y':1},

                            )
            } 

#TAB 4
#Distance Output
@app.callback(
    Output('distance', 'children'),
    [Input('origin_airport', 'value'),
     Input('destination_airport', 'value'),
     ])
def update_output_dist(origin, dest):
    dist = df[(df['ORIGIN_AIRPORT']==origin)&(df['DESTINATION_AIRPORT']==dest)].DISTANCE.mean()
    return str(dist)

#Airtime Output
@app.callback(
    Output('airtime', 'children'),
    [Input('origin_airport', 'value'),
     Input('destination_airport', 'value'),
     ])
def update_output_airtime(origin, dest):
    dist = df[(df['ORIGIN_AIRPORT']==origin)&(df['DESTINATION_AIRPORT']==dest)].AIR_TIME.mean()
    return str(dist)

#Schedule_Time Output
@app.callback(
    Output('sched_time', 'children'),
    [Input('origin_airport', 'value'),
     Input('destination_airport', 'value'),
     ])
def update_output_st(origin, dest):
    dist = df[(df['ORIGIN_AIRPORT']==origin)&(df['DESTINATION_AIRPORT']==dest)].SCHEDULED_TIME.mean()
    return str(dist)

#prediction Output
@app.callback(
    Output('outputPredict', 'children'),
    [Input('buttonPredict', 'n_clicks')],
    [State('origin_airport', 'value'), 
    State('destination_airport', 'value'),
    State('depart_day', 'value'),
    State('depart_month', 'value'),
    State('depart_hour', 'value'),
    State('arr_day', 'value'),
    State('arr_month', 'value'),
    State('arr_hour', 'value'),
    ])
def update_output(n_clicks, origin, dest, depart_day, depart_month, depart_hour, arr_day, arr_month, arr_hour):
    dist = df[(df['ORIGIN_AIRPORT']==origin)&(df['DESTINATION_AIRPORT']==dest)].DISTANCE.mean()
    airtime = df[(df['ORIGIN_AIRPORT']==origin)&(df['DESTINATION_AIRPORT']==dest)].AIR_TIME.mean()
    sched_time = df[(df['ORIGIN_AIRPORT']==origin)&(df['DESTINATION_AIRPORT']==dest)].SCHEDULED_TIME.mean()
    data = np.array([[dist,depart_day,depart_month,depart_hour,arr_day,arr_month,arr_hour,airtime,sched_time]])
    prediction = loadModel.predict(data)
    predictProba = loadModel.predict_proba(data)
    hasil = ''
    if(prediction[0] == 1) :
        hasil = 'Delayed' 
    else :
        hasil = 'Normal'
    return 'Prediction : ' + hasil + '  Delay Probability : ' + str(predictProba[0,1])


if __name__ == '__main__':
    app.run_server(debug=True,port=1996)