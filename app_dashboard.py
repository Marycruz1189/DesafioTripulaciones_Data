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
from tensorflow import keras
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import streamlit as st
from streamlit_folium import folium_static
import folium

dir = os.path.dirname

path = dir(os.path.abspath(__file__))
sys.path.append(path)
print(sys.path)

from utils.streamlit_functions import ad_markers
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



menu = st.sidebar.selectbox('Menu:',
            options=["Distribution map", "Metrics"])


if menu == 'Distribution map':
    st.cache()

    add_selectbox = st.sidebar.selectbox('Select a city:', options= ['Madrid', 'Barcelona', 'Sevilla', 'Valencia', 'Malaga', 'Bilbao'])
    if add_selectbox == 'Madrid':
        Spain = folium.Map(location=[40.41261279333637, -3.6978350022976505], zoom_start= 12)
        ad_markers(df_madrid, 'lon', 'lat', Spain)
        folium_static(Spain)
    if add_selectbox == 'Barcelona':
        Spain = folium.Map(location=[41.395186244087334, 2.1762772551305165], zoom_start=12)
        ad_markers(df_barcelona, 'lon', 'lat', Spain)
        folium_static(Spain)
    if add_selectbox == 'Sevilla':
        Spain = folium.Map(location=[37.38731786603002, -5.98418119408731], zoom_start= 12)
        ad_markers(df_sevilla, 'lon', 'lat', Spain)
        folium_static(Spain)
    if add_selectbox == 'Valencia':
        Spain = folium.Map(location=[39.47245434226027, -0.38000370078274004], zoom_start= 12)
        ad_markers(df_valencia, 'lon', 'lat', Spain)
        folium_static(Spain)
    if add_selectbox == 'Malaga':
        Spain = folium.Map(location=[36.719856985428834, -4.421070372558391], zoom_start= 12)
        ad_markers(df_malaga, 'lon', 'lat', Spain)
        folium_static(Spain)
    if add_selectbox == 'Bilbao':
        Spain = folium.Map(location=[43.263003186179645, -2.935033196603242], zoom_start= 12)
        ad_markers(df_bilbao, 'lon', 'lat', Spain)
        folium_static(Spain)
        
if menu == 'Metrics':
    st.write('Aquí podemos implementar métricas sobre actividad de los usuarios...etc')


    
