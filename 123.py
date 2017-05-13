import plotly
plotly.tools.set_credentials_file(username='ViktorS', api_key='gk3itQcWHuFkAfuZleor')

# import plotly.plotly as py
# import plotly.graph_objs as go

# from datetime import datetime
# x = [datetime(year=2016, month=9, day=23),
#      datetime(year=2016, month=9, day=24),
#      datetime(year=2016, month=9, day=25)]

# data = [go.Scatter(x=x,y=[142, 50, 8])]
# py.plot(data)




# import os

# import plotly.offline as offline
# import plotly.graph_objs as go

# offline.plot({'data': [{'y': [4, 2, 3, 4]}],
#                'layout': {'title': 'Test Plot TOPKEK',
#                           'font': dict(size=16)}},
#              image='png',
#              filename='__pycache__/TOPKEK')




import plotly.plotly as py
import plotly.graph_objs as go

trace = go.Bar(x=[2, 4, 6], y= [10, 12, 15])
data = [trace]
layout = go.Layout(title='A Simple Plot', width=800, height=640)
fig = go.Figure(data=data, layout=layout)

py.image.save_as(fig, filename='__pycache__/a-simple-plot.png')