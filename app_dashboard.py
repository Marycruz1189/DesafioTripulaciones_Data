from flask import Flask, flash, request, render_template, redirect, url_for
from posixpath import sep
import flask
import pandas as pd
import folium
import numpy as np
import altair as alt
from PIL import Image
import os
import json
import sys
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import streamlit as st
from streamlit_folium import folium_static
import folium
from streamlit_plotly_events import plotly_events

dir = os.path.dirname

path = dir(os.path.abspath(__file__))
sys.path.append(path)
print(sys.path)

from utils.streamlit_functions import ad_markers
from utils.streamlit_functions import read_json
from utils.visualization import users_pie_chart
from utils.visualization import scatter
from utils import sql_tb as sql

# connection to sql

sql_json_readed = read_json(path + os.sep + 'utils' + os.sep + 'settings_sql.json')
IP_DNS = sql_json_readed["IP_DNS"]
USER = sql_json_readed["USER"]
PASSWORD = sql_json_readed["PASSWORD"]
BD_NAME = sql_json_readed["BD_NAME"]
PORT = sql_json_readed["PORT"]
mysql_db = sql.MySQL(IP_DNS=IP_DNS, USER=USER, PASSWORD=PASSWORD, BD_NAME=BD_NAME, PORT=PORT)
mysql_db.connect()
db_connection_str = mysql_db.SQL_ALCHEMY
db_connection = create_engine(db_connection_str)
users = pd.read_sql('SELECT * FROM users', con=db_connection)
locales = pd.read_sql('SELECT * FROM locales', con= db_connection)

df_madrid = locales.loc[locales['CIUDAD'] == 'Madrid']
df_barcelona = locales.loc[locales['CIUDAD'] == 'Barcelona']
df_bilbao = locales.loc[locales['CIUDAD'] == 'Bilbao']
df_malaga = locales.loc[locales['CIUDAD'] == 'Málaga']
df_sevilla = locales.loc[locales['CIUDAD'] == 'Sevilla']
df_valencia = locales.loc[locales['CIUDAD'] == 'Valencia']


"""
se usaba como ejemplo antes de tener las tablas subidas a sql

madrid_path = path + os.sep + 'data' + os.sep + 'madrid.csv'
barcelona_path = path + os.sep + 'data' + os.sep + 'barcelona.csv'
bilbao_path = path + os.sep + 'data' + os.sep + 'bilbao.csv'
malaga_path = path + os.sep + 'data' + os.sep + 'malaga.csv'
sevilla_path = path + os.sep + 'data' + os.sep + 'sevilla.csv'
valencia_path = path + os.sep + 'data' + os.sep + 'valencia.csv'
df_madrid = pd.read_csv(madrid_path)
df_barcelona = pd.read_csv(barcelona_path)
df_bilbao = pd.read_csv(bilbao_path)
df_malaga = pd.read_csv(malaga_path)
df_sevilla = pd.read_csv(sevilla_path)
df_valencia = pd.read_csv(valencia_path)
"""


menu = st.sidebar.selectbox('Menu:',
            options=["Distribution map", "Metrics"])


if menu == 'Distribution map':
    st.cache()

    add_selectbox = st.sidebar.selectbox('Select a city:', options= ['Madrid', 'Barcelona', 'Sevilla', 'Valencia', 'Malaga', 'Bilbao'])
    
    if add_selectbox == 'Madrid':
        Spain = folium.Map(location=[40.41261279333637, -3.6978350022976505], zoom_start= 12)
        ad_markers(df_madrid, 'LONGITUD', 'LATITUD', Spain)
        folium_static(Spain)
    if add_selectbox == 'Barcelona':
        Spain = folium.Map(location=[41.395186244087334, 2.1762772551305165], zoom_start=12)
        ad_markers(df_barcelona, 'LONGITUD', 'LATITUD', Spain)
        folium_static(Spain)
    if add_selectbox == 'Sevilla':
        Spain = folium.Map(location=[37.38731786603002, -5.98418119408731], zoom_start= 12)
        ad_markers(df_sevilla, 'LONGITUD', 'LATITUD', Spain)
        folium_static(Spain)
    if add_selectbox == 'Valencia':
        Spain = folium.Map(location=[39.47245434226027, -0.38000370078274004], zoom_start= 12)
        ad_markers(df_valencia, 'LONGITUD', 'LATITUD', Spain)
        folium_static(Spain)
    if add_selectbox == 'Malaga':
        Spain = folium.Map(location=[36.719856985428834, -4.421070372558391], zoom_start= 12)
        ad_markers(df_malaga, 'LONGITUD', 'LATITUD', Spain)
        folium_static(Spain)
    if add_selectbox == 'Bilbao':
        Spain = folium.Map(location=[43.263003186179645, -2.935033196603242], zoom_start= 12)
        ad_markers(df_bilbao, 'LONGITUD', 'LATITUD', Spain)
        folium_static(Spain)
    
    #tipo_selectbox = st.sidebar.selectbox('local type', options=['all','restaurant', 'bar', 'pub', 'cafe', 'cinema', 'theatre'])
    #if tipo_selectbox == 'restaurant' and add_selectbox == 'Madrid':
        #rest_df = 


if menu == 'Metrics':
    
    metrics_opt = st.sidebar.selectbox('options:', options= ['tabla users', 'distribucion usuarios', 'distribucion discapacidades', 'relacion valoraciones grado discapacidad', 'tabla locales'])
    if metrics_opt == 'tabla users':
        st.table(users)
    if metrics_opt == 'distribucion usuarios':
        ciudad = plotly_events(users_pie_chart(users, 'CIUDAD'))
    if metrics_opt == 'distribucion discapacidades':
        dist_dicap = plotly_events(users_pie_chart(users, 'disability'))
    if metrics_opt ==  'relacion valoraciones grado discapacidad':
        grado_val = plotly_events(scatter(users, 'GRADO', 'FAKE_VAL'))
    if metrics_opt == 'tabla locales':
        st.table(locales)




