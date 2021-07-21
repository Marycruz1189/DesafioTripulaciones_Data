'''
contains the specific functions used for periodic processes
'''
import pandas as pd
import numpy as np
import lxml
import xlrd
import os, sys
import json

dir = os.path.dirname

# se saltan tres veces de directorio para llegar al directorio raíz del proyecto '/Entregable_EDA'
# la primera para eliminar el nombre del archivo 
# las dos siguientes para eliminar los directorios '/utils' y '/src'
src_path = dir(dir(dir(__file__)))

# se incorpora la ruta hasta el directorio raiz al path del archivo
sys.path.append(src_path)

prov_Anda=['18', '23', '11', '14', '21','29','41']
prov_ClM = ['02','13','16','16','19','45']
prov_CyL = ['05','09','24','34','37','40','42','47','49']
prov_Cat = ['08','17','25','43']
prov_CV= ['03','12','46']
prov_Ast = ['33']
prov_Gal = ['15','27','32','36']
prov_CAM = ['28']

def read_json_to_dict(json_fullpath):
    """
    Read a json and return a object created from it.
    Args:
        json_fullpath: json fullpath

    Returns: json object.
    """
    try:
        with open(json_fullpath, 'r+') as outfile:
            json_readed = json.load(outfile)
        return json_readed
    except Exception as error:
        raise ValueError(error)