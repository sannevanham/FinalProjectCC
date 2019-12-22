#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

filename = 'nama_10_gdp_1_Data.csv'

df = pd.read_csv(filename, header = 0, na_values = ':')
def numeric(x):
    y = pd.to_numeric(x, errors='coerce')
    return y
df['Value'] = df['Value'].str.replace('.','')
df['Value'] = df['Value'].str.replace(',', '.')
df['Value'] = df['Value'].apply(numeric)
df.dropna(inplace=True)

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

available_indicators = df['NA_ITEM'].unique()
available_units = df['UNIT'].unique()
available_countries = df['GEO'].unique()

app.layout = html.Div([
    html.H1(children='Final Cloud Computing Project'),
    html.Div([
        html.H1(children='Scatterplot of two indicators'),
        html.H2(children='''Compares different indicators against each other for all countries'''),

        html.Div([
        
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label':i, 'value': i} for i in available_indicators],
                    value = 'Gross domestic product at market prices'
                ),
                dcc.RadioItems(
                    id='xaxis-type',
                    options = [{'label': i,'value': i} for i in ['Linear', 'Log']],
                    value = 'Linear',
                    labelStyle={'display':'inline-block'}
                ),
                dcc.RadioItems(
                    id='unit-value',
                    options = [{'label': i, 'value': i} for i in available_units],
                    value = 'Chain linked volumes, index 2010=100',
                    labelStyle={'display':'inline-block'}
                )
            ],
            style={'width':'48%', 'display':'inline-block'}),
        
            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label':i, 'value':i}for i in available_indicators],
                    value='Value added, gross'
                ),
                dcc.RadioItems(
                    id='yaxis-type',
                    options = [{'label': i,'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display':'inline-block'}
                )
            ],style={'width':'48%','float':'right','display':'inline-block'}),
        ]),
    
        dcc.Graph(id='indicator-graphic'),
    
        dcc.Slider(
            id='year--slider',
            min=df['TIME'].min(),
            max=df['TIME'].max(),
            value=df['TIME'].max(),
            step=None,
            marks={str(year):str(year) for year in df['TIME'].unique()}
        ),
    ]),
    
    html.Div([
        html.H1(),
        html.H1(),
        html.H1(children='Linechart between country and indicator'),
        html.H2(children='''Examines the trend of a certain indicator for a certain country'''),
        
        html.Div([
            dcc.Dropdown(
                id='country-value',
                options=[{'label': i,'value': i} for i in available_countries],
                value = 'Cyprus'
            ),
            dcc.RadioItems(
                id='unit',
                options = [{'label': i, 'value': i} for i in available_units],
                value = 'Chain linked volumes, index 2010=100',
                labelStyle={'display':'inline-block'}
            )
        ], style = {'width': '48%', 'display':'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='indicator',
                options=[{'label': i, 'value':i} for i in available_indicators],
                value = 'Value added, gross'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
        
        dcc.Graph(id='country-indicator')
        
        ])
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('unit-value','value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type, unit_value,
                 year_value):
    dff = df[(df['TIME'] == year_value) & (df['UNIT'] == unit_value)]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.7,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 70, 'b': 40, 't': 10, 'r': 20},
            hovermode='closest',
            legend={'x':0,'y':1},
            clickmode= 'event+select'
        )
    }
@app.callback(
    dash.dependencies.Output('country-indicator', 'figure'),
    [dash.dependencies.Input('country-value', 'value'),
     dash.dependencies.Input('unit','value'),
     dash.dependencies.Input('indicator', 'value')])
def update_line(country_value, unit_v, indicator_column_name):
    dff = df[df['UNIT'] == unit_v]
    
    return {
        'data': [go.Scatter(
            x=dff['TIME'].unique(),
            y=dff[(dff['NA_ITEM'] == indicator_column_name)&(dff['GEO'] == country_value)]['Value'],
            text=dff[dff['NA_ITEM'] == indicator_column_name]['NA_ITEM'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.7,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Years',
                'type': 'linear'
            },
            yaxis={
                'title': indicator_column_name,
                'type': 'linear'
            },
            margin={'l': 70, 'b': 40, 't': 10, 'r': 20},
            hovermode='closest',
            legend={'x':0,'y':1}
        )
    }
if __name__ == '__main__':
    app.run_server()


# In[ ]:




