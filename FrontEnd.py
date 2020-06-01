import plotly.graph_objects as go #or plotly.express as px
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import AppAnalysis as a

#genrestats = a.Appanalysis('Dating', 'Facebook')

fig = go.Figure() #or any Plotly Express Funct

app = dash.Dash(__name__)

ALLOWED_TYPES = ('text', 'number', 'password',
            'email', 'search', 'tel', 'url',
            'range', 'hidden')

app.layout = html.Div(
    [
        html.H2("How Your App Name Will Do In Each Market"),
        html.Div(
        [
            html.P('Fill in the Genre and Name text boxes  ->')
        ], style={'width' : '25%',
              'display' : 'inline-block'
            }
        ),
        dcc.Input(id='input1',
                type=ALLOWED_TYPES[0],
                value='Dating',
                debounce=True),
        dcc.Input(id='input2',
                type=ALLOWED_TYPES[0],
                value='Facebook',
                debounce=True),
        html.Div([
            dcc.Graph(id='whereitgoes')
        ])

    ]
    # ,
    # dcc.Graph(figure=fig)
)



def update_output(input1, input2):
    print(input1)
    print(input2)
    if ((len(input1) > 0) & (len(input2) > 0)):
        genrestats = a.Appanalysis(input1, input2)
        allmeans = []
        ymeans = []
        for g in genrestats:
            allmeans.append(genrestats[g]['mean_of_means'])
            ymeans.append(genrestats[g]['ymean'])
        w = 0.3
        trace1 = go.Bar(x=list(genrestats.keys()), y=allmeans)
        trace2 = go.Bar(x=list(genrestats.keys()), y=ymeans)
        return {
                'data' : [trace1, trace2],
                'type' : 'bar',
                'name' : 'App Analysis Graph',
                'layout' : go.Layout(title=genre, barmode='stack')
                }
    else:
        return {'data' : [], 'layout' : go.Layout(title='None', barmode='stack')}


@app.callback(
    Output("whereitgoes", "figure"),
    [Input('input1', 'value'),
     Input('input2', 'value')]
)
def callback(genre, name):
    print('in callback')
    genrestats = a.Appanalysis(genre, name)
    genres = list(genrestats.keys())
    print('___________----------------______________________-------asdfasdfaf')
    print(genres)
    allmeans = [genrestats[g]['mean_of_means'] for g in genrestats ]
    ymeans = [genrestats[g]['ymean'] for g in genrestats ]
    trace1 = {'data' : [
                {
                    'x' : genres,
                    'y' : allmeans,
                    'name' : 'Overall Mean',
                    'type' : 'bar'
                    # 'mode' : 'markers',
                    # 'marker' : {'size' : 12}

                },
                {
                    'x' : genres,
                    'y' : ymeans,
                    'name' : 'Your Mean',
                    'type' : 'bar'
                    # 'mode' : 'markers',
                    # 'marker' : {'size' : 15}

                }
            ],
            'layout' : go.Layout(title='Your App Rating Relative To Each Genre',
                    barmode = 'group')
        }
    return trace1
        #     {'data': [
        #         {
        #             'x': [1, 2, 3, 4],
        #             'y': [4, 1, 3, 5],
        #             'text': ['a', genre, name, 'd'],
        #             'customdata': ['c.a', 'c.b', 'c.c', 'c.d'],
        #             'name': 'Trace 1',
        #             'mode': 'markers',
        #             'marker': {'size': 12}
        #         },
        #         {
        #             'x': [1, 2, 3, 4],
        #             'y': [9, 4, 1, 4],
        #             'text': ['w', 'x', 'y', 'z'],
        #             'customdata': ['c.w', 'c.x', 'c.y', 'c.z'],
        #             'name': 'Trace 2',
        #             'mode': 'markers',
        #             'marker': {'size': 12}
        #         }
        #     ],
        #     'layout' : go.Layout(title='Hi', barmode='stack')
        # }
    #return update_output(genre, name)


#def getFigure(df, genre):

    # f, ax = plt.subplots(figsize=(20,5))
    # ax = plt.bar(list(genrestats.keys()), allmeans, width=0.4, color='red', label='Overall', alpha=1)
    # ax = plt.bar(list(genrestats.keys()), ymeans, width=-0.4, color='gray', label='Yours', alpha=1)
    # plt.xticks(rotation=63)
    # plt.title('Your App Name Rating Relative to Each Genre (less red the better)')
    # # ax1.legend('Overall')
    # # ax2.legend('Yours')
    # plt.figure(figsize=(1,15))
    # plt.show();


app.run_server(debug=True, use_reloader=False)
