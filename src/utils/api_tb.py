#Este archivo contiene la funcionalidad asociada al trabajo con APIs.
from flask import Flask, request, render_template
import os, sys
import json


def main(main_path,app):
    """Esta función inicia el proceso de ejecución del app a partir de la información que se recibe de un .json que se 
    situa en un lugar referenciado al path desde donde ejecutamos la función"""
    print("---------STARTING PROCESS---------")
    print(__file__)
    
    """Estos valores llevan al path donde se encuentra el .json, referenciados al path desde donde se ejecuta."""
    settings_file = main_path + os.sep + "settings.json"
    print(settings_file)
    
    """Esta sección carga el .json"""
    with open(settings_file, 'r+') as outfile:
        json_readed = json.load(outfile)
    
    
    """Esta sección define lo que se encuentra en el .json como argumentos para la correr la app"""
    DEBUG = json_readed["debug"]
    HOST = json_readed["host"]
    PORT_NUM = json_readed["port"]
    app.run(debug=DEBUG, host=HOST, port=PORT_NUM)