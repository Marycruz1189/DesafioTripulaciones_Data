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

path = dir(dir(os.path.abspath(__file__)))
sys.path.append(path)
print(sys.path)

from utils.streamlit_functions import ad_markers
from utils.streamlit_functions import read_json
from utils.visualization import users_pie_chart
from utils.visualization import scatter
from utils import mysql_driver as sql

# generación de la entidad de conexión a la BDD 
sql_json_readed = read_json(path + os.sep + 'utils' + os.sep + 'settings_sql.json')
IP_DNS = sql_json_readed["IP_DNS"]
USER = sql_json_readed["USER"]
PASSWORD = sql_json_readed["PASSWORD"]
BD_NAME = sql_json_readed["BD_NAME"]
PORT = sql_json_readed["PORT"]
mysql_db = sql.MySQL(IP_DNS=IP_DNS, USER=USER, PASSWORD=PASSWORD, BD_NAME=BD_NAME, PORT=PORT)

# Conexión y extracción de los datos de la BDD y cierre de conexión
mysql_db.connect()
db_connection_str = mysql_db.SQL_ALCHEMY
db_connection = create_engine(db_connection_str)
df_users = pd.read_sql('SELECT * FROM users', con=db_connection)
df_locales = pd.read_sql('SELECT * FROM locales', con= db_connection)
df_valoraciones = pd.read_sql('SELECT * FROM valoraciones', con= db_connection)
mysql_db.close()

# Modificaciones a los datos de la BDD 
# Modificaciones a l
df_locales['ACUM_VERDE'] = df_locales['ACUM_VERDE'].apply(lambda x: int(x))
df_locales['ACUM_AMARILLO'] = df_locales['ACUM_AMARILLO'].apply(lambda x: int(x))
df_locales['ACUM_ROJO'] = df_locales['ACUM_ROJO'].apply(lambda x: int(x))
df_locales.rename(columns = {'LATITUD':'lat', 'LONGITUD':'lon'}, inplace = True)


def get_icon_color (green, red, yellow):
    if green >= red and green >= yellow:
        return 'green'
    elif red >= green and red >= yellow:
        return 'red'
    elif yellow >= red and yellow >= green:
        return 'beige'

def get_icon_sign(tipo_local):
    if tipo_local == 'restaurantes':
        return 'glyphicon-home'
    elif tipo_local == 'bar':
        return 'glyphicon-glass'
    elif tipo_local == 'cine':
        return 'glyphicon-facetime-video'
    elif tipo_local == 'cafe':
        return 'glyphicon-glass'
    elif tipo_local == 'pub':
        return 'glyphicon-volume-up'
    elif tipo_local == 'teatro':
        return 'glyphicon-user'

menu = st.sidebar.selectbox('Menu:', options=["Locales", "Tablas"])

if menu == 'Locales':
    st.cache()
    #df_locales_plot = df_locales

# filtro de locales por ciudad
    cities = list(df_locales['CIUDAD'].unique())
    cities.append('N/A')
    city_selectbox = st.sidebar.selectbox ('Ciudad:', options= cities, index= 6)
    if city_selectbox == 'Madrid':
        Spain = folium.Map(location=[40.45261279333637, -3.6778350022976505], zoom_start= 12)
    elif city_selectbox == 'Barcelona':
        Spain = folium.Map(location=[41.405186244087334, 2.1762772551305165], zoom_start=12)
    elif city_selectbox == 'Sevilla':
        Spain = folium.Map(location=[37.38731786603002, -5.98418119408731], zoom_start= 12)
    elif city_selectbox == 'Valencia':
        Spain = folium.Map(location=[39.47245434226027, -0.38000370078274004], zoom_start= 12)
    elif city_selectbox == 'Málaga':
        Spain = folium.Map(location=[36.719856985428834, -4.421070372558391], zoom_start= 12)
    elif city_selectbox == 'Bilbao':
        Spain = folium.Map(location=[43.299503186179645, -2.935033196603242], zoom_start= 12)
    else:
        Spain = folium.Map(location=[40.41261279333637, -3.6978350022976505], zoom_start= 6)

# filtro por certificados
    certif = df_locales.CERTIFICACION.unique().tolist()
    certif.append('N/A')
    certif_selectbox = st.sidebar.selectbox('Certificación:', options=certif, index=2)

# filtro de locales por sector
    sectores = df_locales.SECTOR.unique().tolist()
    sectores.append('N/A')
    sect_selectbox = st.sidebar.selectbox('Sector:', options=sectores, index=2)

# filtro de locales por tipo
    tipo_selectbox = st.sidebar.multiselect('Tipo de local:', options=df_locales.TIPO.unique().tolist())

# filtro por valoraciones 
    # valoraciones verdes
    val_verde = st.sidebar.select_slider("Selección de rango de valoraciones verdes", options=range(min(df_locales.iloc[:, 15]), max(df_locales.iloc[:, 15]) + 1),
                                      value=(min(df_locales.iloc[:, 15]), max(df_locales.iloc[:, 15])))
    val_verde_min = min(df_locales.iloc[:, 15])
    val_verde_max = max(df_locales.iloc[:, 15])

    # valoraciones amarillas
    val_amarilla = st.sidebar.select_slider("Selección de rango de valoraciones amarillas", options=range(min(df_locales.iloc[:, 16]), max(df_locales.iloc[:, 16]) + 1),
                                      value=(min(df_locales.iloc[:, 16]), max(df_locales.iloc[:, 16])))
    val_amar_min = min(df_locales.iloc[:, 16])
    val_amar_max = max(df_locales.iloc[:, 16])

    # valoraciones rojas
    val_roja = st.sidebar.select_slider("Selección de rango de valoraciones rojas", options=range(min(df_locales.iloc[:, 17]), max(df_locales.iloc[:, 17]) + 1),
                                      value=(min(df_locales.iloc[:, 17]), max(df_locales.iloc[:, 17])))
    val_roja_min = min(df_locales.iloc[:, 17])
    val_roja_max = max(df_locales.iloc[:, 17])

# aplicacion de los filtros
    if certif_selectbox != 'N/A':
        df_locales = df_locales.loc[df_locales['CIUDAD'] == city_selectbox]

    if certif_selectbox == 'Y':
        df_locales = df_locales.loc[df_locales['CERTIFICACION'] == 'Y']
    elif certif_selectbox == 'N':
        df_locales = df_locales.loc[df_locales['CERTIFICACION'] == 'N']

    if sect_selectbox != 'N/A':
        df_locales = df_locales.loc[df_locales['SECTOR'] == sect_selectbox]

    if len(tipo_selectbox) != 0:
        df_locales = df_locales.loc[df_locales['TIPO'].isin(tipo_selectbox), :]

    if val_verde_min != val_verde[0] or val_verde_max != val_verde[1]:
        df_locales = df_locales.loc[(df_locales['ACUM_VERDE'] >= val_verde[0]) & (df_locales['ACUM_VERDE'] <= val_verde[1]), :]

    if val_amar_min != val_amarilla[0] or val_amar_max != val_amarilla[1]:
        df_locales = df_locales.loc[(df_locales['ACUM_AMARILLO'] >= val_amarilla[0]) & (df_locales['ACUM_AMARILLO'] <= val_amarilla[1]), :]

    if val_roja_min != val_roja[0] or val_roja_max != val_roja[1]:
        df_locales = df_locales.loc[(df_locales['ACUM_ROJO'] >= val_roja[0]) & (df_locales['ACUM_ROJO'] <= val_roja[1]), :]

# Salida de los datos
    # pintar locales
    # ad_markers(df_locales, 'lon', 'lat', Spain)
    for i in range(len(df_locales)):
        icon_color = get_icon_color(df_locales['ACUM_VERDE'].iloc[i],df_locales['ACUM_ROJO'].iloc[i],df_locales['ACUM_AMARILLO'].iloc[i])
        loc_name = df_locales['NOMBRE_LOCAL'].iloc[i]
        icon_sign = get_icon_sign(df_locales['TIPO'].iloc[i])
        folium.Marker([df_locales['lat'].iloc[i], df_locales['lon'].iloc[i]], popup=loc_name, icon=folium.Icon(color=icon_color,icon=icon_sign)).add_to(Spain)
    folium_static(Spain)

    # extracción de estadísticas
    if city_selectbox == 'N/A':
        ciudad_chart = plotly_events(users_pie_chart(df_locales, 'CIUDAD'))
    tipo_chart = plotly_events(users_pie_chart(df_locales, 'TIPO'))
    # ciudad_chart = plotly_events(users_pie_chart(df_locales, 'SECTOR'))
    val_scatter_green = plotly_events(scatter(df_locales, 'ACUM_VERDE', 'TIPO'))
    val_scatter_yellow = plotly_events(scatter(df_locales, 'TIPO', 'ACUM_AMARILLO'))
    val_scatter_red= plotly_events(scatter(df_locales, 'ACUM_ROJO', 'TIPO'))
    '''
    if metrics_opt == 'distribucion discapacidades':
        dist_dicap = plotly_events(users_pie_chart(users, 'disability'))
    if metrics_opt ==  'relacion valoraciones grado discapacidad':
    '''


if menu == 'Tablas':    
    metrics_opt = st.sidebar.selectbox('options:', options= ['tabla users', 'tabla locales','tabla valoraciones']) # ,'distribucion usuarios', 'distribucion discapacidades', 'relacion valoraciones grado discapacidad', 'tabla locales'])
    if metrics_opt == 'tabla users':
        st.table(df_users)
    elif metrics_opt == 'tabla locales':
        st.table(df_locales)
    elif metrics_opt == 'tabla valoraciones':
        st.table(df_valoraciones)
     