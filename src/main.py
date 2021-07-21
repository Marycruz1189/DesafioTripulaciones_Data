"""
Siempre que veas 'pass' es un TO-DO (por hacer)

"""

"""1"""


import os
import sys


# Llama a la función 'mi_funcion' que está en /flask/api.py. No puede dar error.
path = os.path.abspath(__file__) 
dir = os.path.dirname

path =dir(path) + os.sep + "flask"
 
sys.path.append(path)
import api

print(api.mi_funcion)
