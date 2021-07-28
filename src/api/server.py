from flask import Flask, request, render_template
import os, sys
import argparse
import pandas as pd
from sqlalchemy import create_engine

#Para correr este archivo es necesario abrir el cmd y aplicar la ruta a este archivo.
#A continuación se ejecuta el comando server.py -x 8642 y cogemos la ruta http que se indica.
#Seguidamente seguimos las instrucciones que indica la página. La contraseña es M21755015


# ---------- Append de ruta ----------
"""Con este comando de 5 líneas añadimos al archivo la ruta a la carpeta src, que contiene utils.
que nos valdrá para importar las funciones que utilizaremos para generar la API."""

if __name__ == '__main__':
    dir = os.path.dirname
    path = dir(dir(os.path.abspath(__file__)))
    sys.path.append(path)
    print(sys.path)

    import utils.api_tb as api
    from utils import mysql_driver as sql
    from utils.streamlit_functions import read_json   

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


app = Flask(__name__)   

# ---------- Funciones flask ----------

@app.route("/")  
def home():

    return df_locales.to_json()

# ---------- Llamada función inicio ----------
if __name__ == "__main__":
    api.main(main_path = dir(__file__), app=app)