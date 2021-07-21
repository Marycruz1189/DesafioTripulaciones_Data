import folium
import pandas

def ad_markers(dataframe, long, lat, map):
    #for i in range(len(dataframe)):
    if len(dataframe) < 1000:
        for i in range(len(dataframe)):
            folium.Marker([dataframe.iloc[i][lat], dataframe.iloc[i][long]], popup=[dataframe.iloc[i]['tipo'],dataframe.iloc[i]['name']]).add_to(map)
        return
    else:
        for i in range(1000):
            folium.Marker([dataframe.iloc[i][lat], dataframe.iloc[i][long]], popup=[dataframe.iloc[i]['tipo'],dataframe.iloc[i]['name']]).add_to(map)
        return
    