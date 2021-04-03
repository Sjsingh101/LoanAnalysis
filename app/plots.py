import plotly.express as px
import plotly.graph_objs as go

def plotbar(x,y,title,xtitle,ytitle):
    return px.bar( 
                x=x,
                y=y,
                ).update_layout(
                title={
                    'text': title,
                    'y':0.93,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                xaxis_title=xtitle,
                yaxis_title=ytitle,
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="RebeccaPurple"
                ))

def plotpie(values,names,title):
    return px.pie(
            values=values, 
            names=names).update_layout(
                title={
                    'text': title,
                    'y':0.95,
                    'x':0.45,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="RebeccaPurple"
                ))

def plotbox(y,title,xtitle):
    data = px.box(
            x=y, 
            labels={"x":xtitle}
            ).update_layout(
                title={
                    'text': title,
                    'y':0.95,
                    'x':0.45,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="RebeccaPurple"
                ))
    return data

def lineplot(df,title,xtitle,ytitle):
    return px.line( df,
                    ).update_layout(
                        title={
                            'text': title,
                            'y':0.93,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                        xaxis_title=xtitle,
                        yaxis_title=ytitle,
                        font=dict(
                            family="Courier New, monospace",
                            size=18,
                            color="RebeccaPurple"
                        ))