from flask import Flask, flash, request, render_template, redirect, url_for
import pandas as pd
import os
import json

import sys
dir = os.path.dirname
src_path = dir(dir(__file__))
sys.path.append(src_path)


# Mandatory
app = Flask(__name__)  # __name__ --> __main__ 
"""
Crea una API flask con un solo endpoint que muestre por pantalla el json 'googleplaystore.json'
de la carpeta /data. En resumen, el endpoint tiene que leer el fichero 'googleplaystore.json' y retornarlo.

Además, este fichero contiene otra función que está fuera de la funcionalidad de la API flask

"""
@app.route("/")
def home():
    fullpath = dir(dir(os.path.dirname(__file__))) + os.sep + 'data' + os.sep + "googleplaystore.json"
    with open(fullpath, "r") as json_file_readed:
        json_readed = json.load(json_file_readed)
  
    
    return json_readed                                                                                                                                                           
 
     
""" 1: No es una función de flask"""


def main():
    
    fullpath = dir(dir(os.path.dirname(__file__)))+ os.sep + 'config' + os.sep + "flask_settings.json"
    with open(fullpath, "r") as json_file_readed:
        json_readed = json.load(json_file_readed)     

    # Load variables from jsons
    SERVER_RUNNING = json_readed["server_running"]

    if SERVER_RUNNING:
        DEBUG = json_readed["debug"]
        HOST = json_readed["host"]
        PORT_NUM = json_readed["port"]
        app.run(debug=DEBUG, host=HOST, port=PORT_NUM)


""" PARTE PURA DE FLASK """
if __name__ == '__main__':
    """ Todo lo que está aquí debajo tiene que ver con la funcionalidad del flask """
    
    main()
 