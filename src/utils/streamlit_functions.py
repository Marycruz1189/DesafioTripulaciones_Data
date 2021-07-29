import folium
import pandas
import json

def ad_markers(dataframe, long, lat, map):
    #for i in range(len(dataframe)):
    if len(dataframe) < 1000:
        for i in range(len(dataframe)):
            folium.Marker([float(dataframe.iloc[i][lat]), float(dataframe.iloc[i][long])], popup=[dataframe.iloc[i]['TIPO'],dataframe.iloc[i]['NOMBRE_LOCAL']]).add_to(map)
        return
    else:
        for i in range(1000):
            folium.Marker([float(dataframe.iloc[i][lat]), float(dataframe.iloc[i][long])], popup=[dataframe.iloc[i]['TIPO'],dataframe.iloc[i]['NOMBRE_LOCAL']]).add_to(map)
        return
    
def read_json(fullpath):
    with open(fullpath, "r") as json_file_readed:
        json_readed = json.load(json_file_readed)
    return json_readed

def get_local_icon_color (green, red, yellow):
    if green >= red and green >= yellow:
        return 'green'
    elif red >= green and red >= yellow:
        return 'red'
    elif yellow >= red and yellow >= green:
        return 'beige'

def get_local_icon_sign(tipo_local):
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

def get_user_icon_sign(disability):
    if disability == 'auditiva':
        return 'glyphicon-headphones'
    elif disability == 'ninguna':
        return 'glyphicon-user'
    elif disability == 'motora':
        return 'glyphicon-road'
    elif disability == 'orgánica':
        return 'glyphicon-leaf'
    elif disability == 'cognitiva':
        return 'glyphicon-cog'
    elif disability == 'visual':
        return 'glyphicon-eye-close'


def get_user_icon_color(grado):
    if int(grado) == 0:
        return 'green'
    elif int(grado) > 0 and int(grado) < 50:
        return 'beige'
    elif int(grado) > 50:
        return 'red'