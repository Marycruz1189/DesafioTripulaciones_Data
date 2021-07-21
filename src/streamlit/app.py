import streamlit as st
from PIL import Image
import json
import os
import sys
import pandas as pd
import requests
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest
from sklearn import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
dir = os.path.dirname
src_path = dir(dir(os.path.abspath(__file__)))
sys.path.append(src_path)
from utils.ml import machine_functions

# Haz que se pueda importar correctamente estas funciones que están en la carpeta utils/

dir = os.path.dirname
src_path = dir(dir(os.path.abspath(__file__)))
sys.path.append(src_path)


#from utils.example_abspath import muestra_abspath
from utils.stream_config import draw_map
from utils.dataframes import load_csv_for_map
#from flask.api import 

menu = st.sidebar.selectbox('Menu:',
            options=["No selected", "Load Image", "Map", "API", "MySQL", "Machine Learning"])

if menu == "No selected": 
    #test = "C:\Users\Mary\Desktop\BootCamp\Python\MaryC-MezaR\data_science_bootcamp_2021\week11_unsupervised_\day2_complete_problem\TOTUM_REVOLUTUM_complete_exercise\config\config.json"
    fullpath = dir(dir(dir(os.path.abspath(__file__)))) + os.sep + 'config' + os.sep + "config.json"
    
    with open(fullpath, "r") as json_file_readed:
        json_readed = json.load(json_file_readed)

    st.title(json_readed['Title'])
         
    # Pon el título del proyecto que está en el archivo "config.json" en /config
        # Pon la descripción del proyecto que está en el archivo "config.json" en /config
    st.write(json_readed['Description'])
    
if menu == "Load Image": 
    """3"""
    img = dir(dir(os.path.dirname(__file__))) + os.sep + 'data' + os.sep + 'img' + os.sep + "happy.jpg"
    # Carga la imagen que está en data/img/happy.jpg
    image = Image.open(img)  
    st.image (image,use_column_width=True)

if menu == "Map":
    """4"""
    csv_map_path = dir(dir(os.path.dirname(__file__))) + os.sep + 'data' + os.sep + os.sep + "red_recarga_acceso_publico_2021.csv"
    # El archivo que está en data/ con nombre 'red_recarga_acceso_publico_2021.csv'
    df_map = load_csv_for_map(csv_map_path)
    draw_map(df_map)

if menu == "API":
     
    url= "http://localhost:6060"
    json_api = pd.read_json(url)
    #tabla = pd.DataFrame.from_dict(json_api)
    st.table(json_api)
    """5"""
    # Accede al único endpoint de tu API flask y lo muestra por pantalla como tabla/dataframe
    

if menu == "MySQL":
    """6"""

    # 1. Conecta a la BBDD

    
    from sqlalchemy import create_engine
    dir = os.path.dirname
    src_path = dir(dir(os.path.abspath(__file__)))
    sys.path.append(src_path)
    import utils.sql_functions as s 

  
    fullpath = dir(dir(dir(os.path.abspath(__file__)))) + os.sep + 'config' + os.sep + "bd_info.json"
    with open(fullpath, "r") as json_file_readed:
        json_readed = json.load(json_file_readed)

    IP_DNS = json_readed["IP_DNS"]
    USER = json_readed["USER"]
    PASSWORD = json_readed["PASSWORD"]
    BD_NAME = json_readed["BD_NAME"]
    PORT = json_readed["PORT"]


    # Connect to MySQL
    mysql_db = s.MySQL(IP_DNS=IP_DNS, USER=USER, PASSWORD=PASSWORD, BD_NAME=BD_NAME, PORT=PORT)
    mysql_db.connect()

    # 2. Obtén, a partir de sentencias SQL (no pandas), la información de las tablas que empiezan por 'fire_archive*' (join)

    select_sql = """SELECT * FROM fire_nrt_M6_96619"""  
                #UNION
                #SELECT * FROM fire_archive_V1_96617"""

    result = mysql_db.execute_get_sql(select_sql)
    df = pd.DataFrame(result)
    st.write(df.head())
    
if menu == "Machine Learning": 
    
# 3. Entrena tres modelos de ML diferentes siendo el target la columna 'fire_type'. Utiliza un pipeline que preprocese los datos con PCA. Usa Gridsearch.  
    machine_functions(df=df)            

    
    

    
    
    
    
    
    # 4. Añade una entrada en la tabla 'student_findings' por cada uno de los tres modelos. 'student_id' es EL-ID-DE-TU-GRUPO.
    # 5. Obtén la información de la tabla 'fire_nrt_M6_96619' y utiliza el mejor modelo para predecir la columna target de esos datos. 
    # 6. Usando SQL (no pandas) añade una columna nueva en la tabla 'fire_nrt_M6_96619' con el nombre 'fire_type_EL-ID-DE-TU-GRUPO'
    # 7. Muestra por pantalla en Streamlit la tabla completa (X e y)
    pass



