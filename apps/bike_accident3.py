import streamlit as st
import pandas as pd
import folium
import geopandas as gpd
from streamlit_folium import folium_static
import pickle
import requests
import re

def app():
    st.title('Accidents - Clusters')
    st.markdown("#### Cluster analysis over the bike accidents between 01.01.2018 and 31.12.2020.")

#   create cluster_gdf (=hotspots) 
    #loading df from csv
    cluster_gdf = pd.read_csv('./data/cluster_gdf.csv')
    #turn polygon column into GeoSeries
    cluster_gdf['polygon'] = gpd.GeoSeries.from_wkt(cluster_gdf['polygon'])
    #
    cluster_gdf = gpd.GeoDataFrame(cluster_gdf, geometry='polygon')
    #
    cluster_gdf = cluster_gdf.drop(columns='Unnamed: 0')
    #
    cluster_gdf.crs = {'init': 'epsg:4326'}    

#   create final_df (=greenlanes) 
    #all API addresses that need to be extracted
    url1 = 'https://www.infravelo.de/api/v1/projects/'
    url2 = 'https://www.infravelo.de/api/v1/projects/50/50/'
    url3 = 'https://www.infravelo.de/api/v1/projects/100/50/'
    url4 = 'https://www.infravelo.de/api/v1/projects/150/50/'
    url5 = 'https://www.infravelo.de/api/v1/projects/200/50/'
    url6 = 'https://www.infravelo.de/api/v1/projects/250/50/'
    #extract all json files as dicts
    response1 = requests.get(url1).json()
    response2 = requests.get(url2).json()
    response3 = requests.get(url3).json()
    response4 = requests.get(url4).json()
    response5 = requests.get(url5).json()
    response6 = requests.get(url6).json()
    #create DataFrame out of all provieded info from API (url1)
    keys = response1['results'][0].keys()
    df1 = pd.DataFrame(columns = keys)
    for i in range(len(response1['results'])):
        df1 = df1.append(response1['results'][i], ignore_index = True)
    #create DataFrame out of all provieded info from API (url2)
    keys = response2['results'][0].keys()
    df2 = pd.DataFrame(columns = keys)
    for i in range(len(response2['results'])):
        df2 = df2.append(response2['results'][i], ignore_index = True)
    #create DataFrame out of all provieded info from API (url3)
    keys = response3['results'][0].keys()
    df3 = pd.DataFrame(columns = keys)
    for i in range(len(response3['results'])):
        df3 = df3.append(response3['results'][i], ignore_index = True)
    #create DataFrame out of all provieded info from API (url4)
    keys = response4['results'][0].keys()
    df4 = pd.DataFrame(columns = keys)
    for i in range(len(response4['results'])):
        df4 = df4.append(response4['results'][i], ignore_index = True)
    #create DataFrame out of all provieded info from API (url5)
    keys = response5['results'][0].keys()
    df5 = pd.DataFrame(columns = keys)
    for i in range(len(response5['results'])):
        df5 = df5.append(response5['results'][i], ignore_index = True)
    #create DataFrame out of all provieded info from API (url6)
    keys = response6['results'][0].keys()
    df6 = pd.DataFrame(columns = keys)
    for i in range(len(response6['results'])):
        df6 = df6.append(response6['results'][i], ignore_index = True)
    #combine all priorly created DataFrames
    frames = [df1, df2, df3, df4, df5, df6]
    green_df = pd.concat(frames)
    # filtering html content
    c = []
    for i in range(len(green_df)):
        single_coor = re.findall('<coordinates>\n\t\t\t\t\t\t\t(.+?)\n\t\t\t\t\t\t</coordinates>', green_df.iloc[i,22])
        c.append(single_coor)
    #
    coor_df = pd.DataFrame(c)
    #
    first_green = pd.DataFrame(coor_df[0]).T
    #
    first_green = first_green.fillna('0,0')
    #
    davy = first_green.T
    type(davy[0][0])
    #
    def crazy(my_string):    
        res = my_string.split(',0 ')
        l = []
        for i, element in enumerate(res):
            res[i] = element.split(',')
            temp_length = len(res[i])
            res2 = []
            for j in range(temp_length):
                #res[i][j] = float(res[i][j])
                res2.insert(0,float(res[i][j]))
                
            if temp_length == 2:    
                l.append(tuple(res2))
        pd.DataFrame(l)
        return l
    #
    final_coor = first_green.T[0].apply(lambda x: crazy(x))
    #
    green_df = green_df.reset_index(drop=True)
    #
    final_df = pd.concat([green_df, final_coor], axis=1)
    #
    final_df = final_df.drop(columns=[
    'costs', 'link', 'companyConstruction', 'apiLink', 'owner',
    'districts', 'milestones', 'types', 'categories', 'image', 
    'imagesCurrent', 'imagesBefore', 'kml', 'additionalInformation', 
    'additionalHtmlContent', ])
    #
    final_df = final_df.rename(columns={0: "coordinates"})
    #
    final_df.status = final_df.status.replace({
    'in Planung': 'in planning', 'Abgeschlossen': 'completed',
    'in Bau': 'under construction', 'Vorgesehen': 'intended' })
    #grouping final_df
    completed = final_df.coordinates[final_df.status == 'completed']
    under_construction = final_df.coordinates[final_df.status == 'under construction']
    in_planning = final_df.coordinates[final_df.status == 'in planning']
    intended = final_df.coordinates[final_df.status == 'intended']

    # creating map
    m = folium.Map(location=[52.52000, 13.4050],tiles='openstreetmap', zoom_start=12)

    # adding accident clusters to map
    folium.features.GeoJson(cluster_gdf,
                            style_function= lambda x: {'fillColor': 'red', 'color': 'red'},
                            tooltip=folium.GeoJsonTooltip(fields= ['count'],aliases=["Accident count: "],labels=True)).add_to(m)

    # adding Greenlanes to map
    folium.PolyLine(locations=completed, color='green', weight=7, opacity=0.7, tooltip='completed').add_to(m)
    folium.PolyLine(locations=under_construction, color='yellow', weight=7, opacity=0.7, tooltip='under construction').add_to(m)
    folium.PolyLine(locations=in_planning, color='orange', weight=7, opacity=0.7, tooltip='in planning').add_to(m)
    folium.PolyLine(locations=intended, color='red', weight=7, opacity=0.7, tooltip='intended').add_to(m)

    # display map
    folium_static(m)

    st.markdown("Accidents clusters were modelled with [DBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html).")
