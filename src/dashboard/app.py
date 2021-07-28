from flask import Flask, flash, request, render_template, redirect, url_for
from posixpath import sep, split
import flask
from folium.map import Tooltip
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
import plotly.express as px

dir = os.path.dirname

path = dir(dir(os.path.abspath(__file__)))
sys.path.append(path)
print(sys.path)

from utils.streamlit_functions import ad_markers
from utils.streamlit_functions import get_local_icon_color
from utils.streamlit_functions import get_local_icon_sign
from utils.streamlit_functions import get_user_icon_color
from utils.streamlit_functions import get_user_icon_sign
from utils.streamlit_functions import read_json
from utils.visualization import users_pie_chart
from utils.visualization import scatter
from utils.visualization import bar
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

menu = st.sidebar.selectbox('Menu:', options=["Locales", 'Usuarios', 'Valoraciones', "Tablas"])

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
    if city_selectbox != 'N/A':
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
    df_locales.rename(columns={'ACUM_VERDE':'Valoraciones verdes', 'ACUM_ROJO':'Valoraciones rojas', 'ACUM_AMARILLO':'Valoraciones amarillas'},inplace=True)
    # pintar locales
    # ad_markers(df_locales, 'lon', 'lat', Spain)
    for i in range(len(df_locales)):
        icon_color = get_local_icon_color(df_locales['Valoraciones verdes'].iloc[i],df_locales['Valoraciones rojas'].iloc[i],df_locales['Valoraciones amarillas'].iloc[i])
        loc_name = df_locales['NOMBRE_LOCAL'].iloc[i]
        icon_sign = get_local_icon_sign(df_locales['TIPO'].iloc[i])
        folium.Marker([df_locales['lat'].iloc[i], df_locales['lon'].iloc[i]], popup=loc_name, icon=folium.Icon(color=icon_color,icon=icon_sign)).add_to(Spain)
    st.title('Mapa de visualización de los locales')
    folium_static(Spain)

    # extracción de estadísticas
    st.title('Análisis de las estadísticas según los filtros seleccionados')
    if city_selectbox == 'N/A':
        st.subheader('Proporción de los locales seleccionados agrupados por localidad')
        ciudad_chart = plotly_events(users_pie_chart(df_locales, 'CIUDAD'))
    st.subheader('Proporción de los locales seleccionados agrupados por tipo de local')
    tipo_chart = plotly_events(users_pie_chart(df_locales, 'TIPO'))

    # análisis de las valoraciones de los locales
    st.subheader('Análisis de los locales según las valoraciones recibidas')
    val_scatter_green = plotly_events(px.scatter(df_locales, 'Valoraciones verdes', 'TIPO', color='CIUDAD'))
    val_scatter_yellow = plotly_events(px.scatter(df_locales, 'Valoraciones amarillas', 'TIPO', color='CIUDAD'))
    val_scatter_red= plotly_events(px.scatter(df_locales, 'Valoraciones rojas', 'TIPO', color='CIUDAD'))

if menu == 'Usuarios':
    st.cache()
# modificación local de la tabla de usuarios    
    df_users = df_users.iloc[:990,:]
    df_users['GRADO'] = df_users['GRADO'].apply(lambda x: int(x))
    df_users['LAT'] = df_users['LAT'].str.replace(',', '.')
    df_users['LON'] = df_users['LON'].str.replace(',', '.')
    df_users.rename(columns={'FAKE_VAL':'VALORACIONES', 'disability':'DISCAPACIDAD'}, inplace=True)
    
    Spain_users = folium.Map(location=[40.41261279333637, -3.6978350022976505], zoom_start= 6)

# filtros
    # filtrar por tipo de discapcidad
    disab = df_users['DISCAPACIDAD'].unique().tolist()
    disab_sel_box = st.sidebar.multiselect('Tipo de discapacidad:',options=disab)

    # filtrar por region
    region = df_users['CA'].unique().tolist()
    region.append('N/A')
    reg_sel_box = st.sidebar.selectbox('seleccionar region:',options= region, index= len(region)-1)

    # filtrar por grado
    sel_grado = st.sidebar.select_slider('seleccionar grado de discapacidad:', options= range(min(df_users.iloc[:,18]), max(df_users.iloc[:,18])+1), value=(min(df_users.iloc[:,18]), max(df_users.iloc[:,18])))
    min_grado = min(df_users['GRADO'])
    max_grado = max(df_users['GRADO'])
    
# aplicación de filtros
    if len(disab_sel_box) != 0:
        df_users = df_users.loc[df_users['DISCAPACIDAD'].isin(disab_sel_box), :]
    if reg_sel_box != 'N/A':
        df_users = df_users.loc[df_users['CA'] == reg_sel_box]
    if min_grado != sel_grado[0] or max_grado != sel_grado[1]:
        df_users = df_users.loc[(df_users['GRADO']>= sel_grado[0]) & (df_users['GRADO']<= sel_grado[1]),:]
    
# salida de los datos
    for i in range(len(df_users)):
        user_icon_color = get_user_icon_color(df_users['GRADO'].iloc[i])
        user_icon_sign = get_user_icon_sign(df_users['DISCAPACIDAD'].iloc[i])
        user_name = df_users['user'].iloc[i]
        folium.Marker([float(df_users['LAT'].iloc[i]), float(df_users['LON'].iloc[i])], popup= user_name, icon= folium.Icon(color=user_icon_color, icon=user_icon_sign)).add_to(Spain_users)
    st.title('Mapa de visualización de los usuarios')
    folium_static(Spain_users)

    st.title('Análisis de las estadísticas según los filtros seleccionados')
    st.subheader('Proporción de usuarios seleccionados agrupados por discapacidad')
    pie_disab = plotly_events(users_pie_chart(df_users, 'DISCAPACIDAD'))
    st.subheader('Agrupación de las valoraciones en función del grado de discapacidadd de usuarios seleccionados')
    val_grado_2 = plotly_events(px.scatter(df_users, 'GRADO', 'VALORACIONES', color='DISCAPACIDAD'))    
    st.subheader('Histograma de valoraciones por discapacidad')
    val_disc = plotly_events(px.bar(df_users, 'DISCAPACIDAD', 'VALORACIONES', color='DISCAPACIDAD'))

if menu == 'Valoraciones':

#transformaciones locales del dataframe
    #df_valoraciones['POR_DISC'] = df_valoraciones['ADD_USU_PORDISC'].apply(lambda x: x.replace(',','.')) 
    df_valoraciones['POR_DISC'] = df_valoraciones['ADD_USU_PORDISC'].apply(lambda x: float('10.22')) 

#filtros
    # filtro de visualización
    visu = st.sidebar.radio("Visualización de los datos por:",('Discapacidad', 'Tipo de local'))
    agreg = st.sidebar.radio("Agregar datos por certificado:",('N', 'S'))

    # filtro por ciudad
    cities = list(df_valoraciones['ADD_LOC_LOCALIDAD'].unique())
    cities.append('N/A')
    city_selectbox = st.sidebar.selectbox ('Ciudad:', options= cities, index= 6)

    # valoraciones con comentario
    comen = ['Y','N','N/A']
    comen_sel_box = st.sidebar.selectbox('Filtrar por valoraciones con comentarios:',options= comen, index= len(comen)-1)

    # filtrar por certificado
    certi = df_valoraciones['ADD_LOC_CERT'].unique().tolist()
    certi.append('N/A')
    certi_sel_box = st.sidebar.selectbox('Filtrar valoraciones por locales certificados:',options= certi, index= len(certi)-1)
    
    # filtro de locales por tipo
    tipo_selectbox = st.sidebar.multiselect('Tipo de local:', options=df_valoraciones.ADD_LOC_CAT.unique().tolist())
    
    # filtrar por tipo de discapcidad
    disab = df_valoraciones['ADD_USU_DISC'].unique().tolist()
    disab_sel_box = st.sidebar.multiselect('Tipo de discapacidad:',options=disab)

# aplicación de los filtros

    if city_selectbox != 'N/A':
        df_valoraciones = df_valoraciones.loc[df_valoraciones['ADD_LOC_LOCALIDAD'] == city_selectbox]
    
    if comen_sel_box != 'N/A':     
        if comen_sel_box == 'Y':
            df_valoraciones = df_valoraciones[df_valoraciones['COMENTARIO'] != '']
        elif comen_sel_box == 'N':
            df_valoraciones = df_valoraciones[df_valoraciones['COMENTARIO'] == '']
    
    if certi_sel_box != 'N/A':     
        if certi_sel_box == 'Y':
            df_valoraciones = df_valoraciones[df_valoraciones['ADD_LOC_CERT']==certi_sel_box]
        elif certi_sel_box == 'N':
            df_valoraciones = df_valoraciones[df_valoraciones['ADD_LOC_CERT']==certi_sel_box]

    if len(tipo_selectbox) != 0:
        df_valoraciones = df_valoraciones.loc[df_valoraciones['ADD_LOC_CAT'].isin(tipo_selectbox), :]

    if len(disab_sel_box) != 0:
        df_valoraciones = df_valoraciones.loc[df_valoraciones['ADD_USU_DISC'].isin(disab_sel_box), :]
    

# generación de un dataframe específico para los datos filtrados
    loc_city_list = df_valoraciones['ADD_LOC_LOCALIDAD'].unique().tolist()
    loc_tip_list = df_valoraciones['ADD_LOC_CAT'].unique().tolist()
    loc_certi_list = df_valoraciones['ADD_LOC_CERT'].unique().tolist()
    usu_disc_list = df_valoraciones['ADD_USU_DISC'].unique().tolist()
    cat_dict = {}

    val_list = []
    for loc_loc in loc_city_list:
        for loc_tip in loc_tip_list:
            for usu_disc in usu_disc_list:
                for loc_certi in loc_certi_list:
                    val = [loc_loc, loc_tip, loc_certi, usu_disc]
                    val.append(len(df_valoraciones[(df_valoraciones['ADD_LOC_CERT']==loc_certi) &(df_valoraciones['ADD_LOC_LOCALIDAD']==loc_loc) & (df_valoraciones['ADD_LOC_CAT']==loc_tip) & (df_valoraciones['ADD_USU_DISC']==usu_disc)]))
                    val_list.append(val)
    df_val = pd.DataFrame(val_list, columns=['Localidad', 'Tipo de Local', 'Certificado', 'Discapacidad', 'Valoraciones'])
    df_val_2 = df_val.groupby(['Tipo de Local','Discapacidad','Certificado']).sum().reset_index()

# salida de los datos
    path_agreg = ['Certificado','Discapacidad','Tipo de Local']
    path_Nagreg = ['Discapacidad','Tipo de Local']
    path_agreg_loc = ['Certificado','Tipo de Local','Discapacidad']
    path_Nagreg_loc = ['Tipo de Local','Discapacidad']

    if city_selectbox == 'N/A':
        st.title('Análisis de las valoraciones')
    else:
        title = 'Análisis de las valoraciones en ' + city_selectbox
        st.title(title)
    if visu == 'Discapacidad' and agreg == 'N':       
        sunburst = plotly_events(px.sunburst(df_val_2,width=700,height= 700, path=path_Nagreg, values='Valoraciones', color='Discapacidad')
                                        , override_height= 700)
        val_barplot = plotly_events(px.bar(df_val_2, 'Valoraciones', 'Discapacidad', color='Tipo de Local', width=675, height=500), override_height=2000)
    elif visu == 'Tipo de local' and agreg == 'N': 
        sunburst = plotly_events(px.sunburst(df_val_2,width=700,height= 700, path=path_Nagreg_loc, values='Valoraciones', color='Tipo de Local')
                                        , override_height= 700)
        val_barplot = plotly_events(px.bar(df_val_2, 'Valoraciones', 'Tipo de Local', color='Discapacidad', width=675, height=500), override_height=2000)
    elif visu == 'Discapacidad' and agreg == 'S':       
        sunburst = plotly_events(px.sunburst(df_val_2,width=700,height= 700, path=path_agreg, values='Valoraciones', color='Discapacidad')
                                        , override_height= 700)
        val_barplot = plotly_events(px.bar(df_val_2, 'Valoraciones', 'Discapacidad', color='Tipo de Local', facet_row='Certificado', width=675, height=500), override_height=2000)
    elif visu == 'Tipo de local' and agreg == 'S': 
        sunburst = plotly_events(px.sunburst(df_val_2,width=700,height= 700, path=path_agreg_loc, values='Valoraciones', color='Tipo de Local')
                                        , override_height= 700)
        val_barplot = plotly_events(px.bar(df_val_2, 'Valoraciones', 'Tipo de Local', color='Discapacidad', facet_row='Certificado', width=675, height=500), override_height=2000)


    
    



    
if menu == 'Tablas':    
    metrics_opt = st.sidebar.selectbox('options:', options= ['tabla users', 'tabla locales','tabla valoraciones']) # ,'distribucion usuarios', 'distribucion discapacidades', 'relacion valoraciones grado discapacidad', 'tabla locales'])
    if metrics_opt == 'tabla users':
        st.table(df_users)
    elif metrics_opt == 'tabla locales':
        st.table(df_locales)
    elif metrics_opt == 'tabla valoraciones':
        st.table(df_valoraciones)

