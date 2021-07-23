import plotly.express as px
import pandas as pd
import streamlit as st
from streamlit_plotly_events import plotly_events

def users_pie_chart(dataframe, measure):
    plot_df = dataframe
    fig = px.pie(plot_df, values= plot_df[measure].value_counts(), names= plot_df[measure].unique())
    return fig

def scatter(dataframe, x, y):
    fig = px.scatter(dataframe, x= x, y= y, title= 'relación grado discapacidad con nº de valoraciones')
    return fig
