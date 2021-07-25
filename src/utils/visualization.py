import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import streamlit as st
from streamlit_plotly_events import plotly_events

def users_pie_chart(dataframe, measure):
    plot_df = dataframe
    fig = px.pie(plot_df, values= plot_df[measure].value_counts(), names= plot_df[measure].unique())
    return fig

def scatter(dataframe, x, y):
    fig = px.scatter(dataframe, x= x, y= y, title= 'relación grado discapacidad con nº de valoraciones', )
    return fig

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="scatter-plot"),
    html.P("Acum_Red:"),
    dcc.RangeSlider(
        id='range-slider',
        min=0, max=50, step=1,
        marks={0: '0', 50: '50'},
        value=[0, 50]
    ),
])

@app.callback(
    Output("scatter-plot", "figure"), 
    [Input("range-slider", "value")])
def update_bar_chart(slider_range):
    low, high = slider_range
    mask = (df['petal_width'] > low) & (df['petal_width'] < high)
    fig = px.scatter(
        df[mask], x="sepal_width", y="sepal_length", 
        color="species", size='petal_length', 
        hover_data=['petal_width'])
    return fig