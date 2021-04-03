from flask import Flask, make_response, request
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from plots import * 
from helper import *
import numpy as np
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

server = Flask(__name__)

minty_bootstrap_css = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/minty/bootstrap.min.css"
app = dash.Dash(__name__, server=server, external_stylesheets=[minty_bootstrap_css])

data = {}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "22rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "24rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("LoanBoard", className="display-4"),
        html.Hr(),
        html.P(
            "Analysis of Loan Payers", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("General", href="/", active="exact"),
                dbc.NavLink("Defaulter", href="/def", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

def psql_connection(database_name, user_name, password, host_name):
    try:
        conn = psycopg2.connect(database=database_name, user=user_name, password=password, host=host_name,port="5432")
        print("Connection Established")
        return conn
    except ConnectionError:
        print("Error in DB connection")
        
def fetch_df(cur):
    cur.execute("select * from loan")
    global data
    data = pd.DataFrame(cur.fetchall(),columns=["grade","defaulter","amount","interest","years","ownership","income","age"])
    return data

def load_data():
    database_name = os.getenv('DB_NAME')
    user_name = os.getenv('DB_USER')
    password = os.getenv('DB_KEY')
    host_name = os.getenv('DB_URL')
    conn = psql_connection(database_name, user_name, password, host_name)
    cur = conn.cursor()
    fetch_df(cur)
    conn.close()

@server.route('/csv', methods=['GET','POST'])
def generate_response():
    load_data()
    resp = make_response(data.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=loan_data_clean.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


@app.callback(
    Output({"type":"gen-bar"}, "figure"), 
    [Input({"type":"ownership-type"}, "value")])
def update_bar_chart(otype):
    gen_dict = Counter(gen_dist(data[data.ownership==otype].age.values))
    gen_names = gen_dict.keys()
    gen_count = gen_dict.values()
    fig = plotbar(gen_names,gen_count,"Generation Wise Ownership","Generation","Count")
    return fig


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    load_data()
    if pathname == "/":
        ownership =  data.ownership.value_counts()
        ownership_type = ownership.index.values
        ownership_count = ownership.values
        def_1 = data[data.defaulter==1].shape[0]
        def_0 = data[data.defaulter==0].shape[0]
        payer_count = np.array([def_0,def_1])
        pvalues = payer_count
        pnames = ["Défrayer", "Defaulters"]
        age_dist = data[data.ownership=="RENT"].age.values

        amt = data.amount
        rate = data.interest
        inc = data.income
        si_ratio = (amt*rate*0.01)/inc 
        srt_si_ratio = sorted(si_ratio)

        return [
                html.H1('General',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=plotbar(ownership_type,ownership_count,
                         "Distribution of Ownership",
                         "Types of Ownership",
                         "Frequency")
                        ),
                dcc.Graph(id={"type":"gen-bar"}),
                dcc.Dropdown(
                        id={"type":"ownership-type"},
                        options=[{"label": x, "value": x} for x in ownership_type],
                        value=ownership_type[0],
                        clearable=False,
                    ),
                dcc.Graph(id='piechart',
                        figure=plotpie(pvalues,pnames,
                        "Types of Payers",
                        )
                    ),
                dcc.Graph(id='boxplot-age',
                        figure=plotbox(age_dist,
                        "Age Distribution","Age of Payers"
                        )
                    ),      
                dcc.Graph(id='boxplot-income',
                        figure=plotbox(srt_si_ratio,
                        "Ratio of total Interest wrt Income Distribution","Total Interest wrt Income"
                        )
                    ),                      
                ]
    elif pathname == "/def":
        df = data[data.defaulter==1]
        grade_dist = df.grade.value_counts()
        df1 = data[data.defaulter==1].grade.value_counts()
        df2 = data.grade.value_counts()
        ratio_def = ((df1/df2)*100)
        #print("R")
        #print(ratio_def.index)
        

        def_ownership =  data[data.defaulter==1].ownership.value_counts()
        def_ownership_type = def_ownership.index.values
        def_ownership_count = def_ownership.values
        return [
                html.H1('Defaulter',
                        style={'textAlign':'center'}),
                dcc.Graph(id='lineplot1',
                         figure=lineplot(
                            grade_dist,
                            "Defaulters Distribution",
                            "Credit Grade",
                            "Count of Defaulters",)
                        ),
                dcc.Graph(id='lineplot2',
                         figure=lineplot(
                            ratio_def,
                            "Defaulters Distribution wrt Whole data",
                            "Credit Grade",
                            "Ratio of Defaulters",)
                        ),
                dcc.Graph(id='defbargraph',
                         figure=plotbar(def_ownership_type,def_ownership_count,
                         "Distribution of Defaulter's Ownership",
                         "Types of Ownership",
                         "Frequency")
                        ),
                    
                ]


    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"{pathname} not exist"),
        ]
    )


if __name__=='__main__':
    load_data()
    app.run_server(host="0.0.0.0",debug=True, port=3000)