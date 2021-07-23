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