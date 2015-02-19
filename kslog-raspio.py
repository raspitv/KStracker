#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in('yourPlotlyID','yourKey')

logfile ='raspio.txt'

read_log = open(logfile, 'r') # open file for reading
lines = read_log.readlines()
read_log.close()  

y_axis = [0,]    # added a 0 to force the point 0,0
x_axis = [0,]    # in both x and y
y_axis2 = []
pc = '%'
project_currency_symbol = '£'
project_currency = 'gbp'

logo_x = 0.87    # set default RasPi.TV annotation positions
logo_y = 0.05
legend_y = 1

# grab the last line and extract hours_into_campaign
hours_into_campaign = float(lines[-1].split(',')[8])
try:
    if lines[-1].split(',')[9]:
        project_currency =  lines[-1].split(',')[9][0:3]
except:
    pass

# here you put some logic to determine project currency symbol
# project_currency_symbol
if project_currency == 'usd':
    project_currency_symbol = '$'

y_title = project_currency_symbol + ' raised'
percent = float(lines[-1].split(',')[1])
day_of_campaign = int((hours_into_campaign / 24) + 1)
campaign_duration = int(float(lines[-1].split(',')[3]))
if day_of_campaign > campaign_duration:
    day_string = 'Campaign Ended'
else:
    day_string = 'Day %d of %d' % (day_of_campaign, campaign_duration)
backers = str(int(lines[-1].split(',')[6]))
backer_string = backers + ' backers'

if percent <= 25:
    logo_y = 0.4
if percent <= 120:
    legend_y = 0.9
percent_string = '%.2f %s of goal' % (percent, pc)
   
if hours_into_campaign >= 72:
    divisor = 24
    title_string = 'RasPiO Duino KS Tracker %s VS days' % project_currency_symbol
    time_unit = 'days'
    x_title = 'Time / days'
else:
    divisor = 1
    title_string = 'RasPiO Duino KS Tracker %s VS hours' % project_currency_symbol
    time_unit = 'hours'
    x_title = 'Time / hours'    

# graph amount raised vs hours/days into campaign
for line in lines:
    amount_raised = int(float(line.split(',')[2]))   # y
    hours_into_campaign = float(line.split(',')[8])  # x
    target = int(float(line.split(',')[0]))
    y_axis.append(amount_raised)
    x_axis.append(round(hours_into_campaign/divisor,4))          # days or hours
    y_axis2.append(target)    
y_axis2.append(target)               # one extra to maintain the correct list length

total_so_far = '%s%d raised' % (project_currency_symbol, amount_raised)

trace0 = Scatter(
    x=x_axis,
    y=y_axis,
    name='Amount Raised'
)
trace1 = Scatter(
    x=x_axis,
    y=y_axis2,
    name='Funding Target'
)

data = Data([trace0,trace1])
layout = Layout(
    paper_bgcolor='#EBFFFF',
    plot_bgcolor='#F5FFFF',
    showlegend=True,
    legend=Legend(
        x=0,
        y=legend_y,
        font=Font(
            family='sans-serif',
            size=12,
            color='#000'
        ),
        bgcolor='#FFE7C6'
    ),
    annotations=Annotations([
        Annotation(
            x=logo_x,
            y=logo_y,
            xref='paper',
            yref='paper',
            xanchor='right',
            yanchor='bottom',
            text='RasPi.TV',
            font=Font(
                family='Arial, sans-serif',
                size=30,
                color='#ff0000'
            ),
            align='center',
            bordercolor='#FFFFFF',
            borderwidth=2,
            borderpad=4,
            bgcolor='#FFFFFF',
            opacity=0.8
        ),
        Annotation(
            x=0.3,           
            y=legend_y,      # level with top of legend
            xref='paper',
            yref='paper',
            xanchor='left',
            yanchor='top',
            text=total_so_far,
            showarrow=False,
        ),
        Annotation(
            x=0.3,
            y=(legend_y - 0.07), # 1 row down from previous
            xref='paper',
            yref='paper',
            xanchor='left',
            yanchor='top',
            text=percent_string,
            showarrow=False,
        ),
        Annotation(
            x=0.3,              
            y=(legend_y - 0.14), # 1 row down from previous
            xref='paper',
            yref='paper',
            xanchor='left',
            yanchor='top',
            text=day_string,
            showarrow=False,
        ),
        Annotation(
            x=0.3,              
            y=(legend_y - 0.21), # 1 row down from previous
            xref='paper',
            yref='paper',
            xanchor='left',
            yanchor='top',
            text=backer_string,
            showarrow=False,
        ),
    ]),
    title=title_string,
    xaxis=XAxis(
        title=x_title,
        titlefont=Font(
            family='Arial, sans-serif',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=YAxis(
        title=y_title,
        titlefont=Font(
            family='Arial, sans-serif',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = Figure(data=data, layout=layout)
unique_url = py.plot(fig, filename = 'raspio-duino')

# for use on server with cron, add your full path to the filename
