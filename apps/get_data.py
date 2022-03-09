import pandas as pd
import geopandas as gpd
import json


def clean_plr(df):
#After reading csv file, cleaning PLR_ID into correct str format
    df['PLR_ID'] = df['PLR_ID'].apply(int)
    df['PLR_ID'] = df['PLR_ID'].apply(lambda x: "0" + str(x) if len(str(x))== 7 else x)
    return df

def round_int(df):
#Make numerical columns on DataFrame into integer
    numerical = df.select_dtypes(include=float).columns.tolist()
    df[numerical] = df[numerical].applymap(lambda x: int(x))
    return df

def round_up(df, num):
#Round up numerical columns on DataFrame with num digit
    numerical = df.select_dtypes(include=float).columns.tolist()
    df[numerical] = df[numerical].applymap(lambda x: round(x, num))
    return df

def read_data(path):
    #Read csv and clean PLR_ID
    df = pd.read_csv(path)
    df = clean_plr(df)

    #Merge it to LOR DataFrame
    #PLR (smallest 542 sub-districts)
    gdf_plr = get_plr()

    _df = gdf_plr.merge(df, how='left', on="PLR_ID")
    df = _df
    df.fillna(0, inplace=True)
    return df

def read_geojson():
    #Read GeoJSON
    f = open('./data/plr.geojson')
    geojson = json.load(f)
    return geojson

def get_plr():
    path_to_data_plr = "./raw_data/LOR_shpfiles/lor_plr.shp"
    gdf_plr = gpd.read_file(path_to_data_plr)
    gdf_plr = clean_plr(gdf_plr)
    return gdf_plr

def get_geojson(area):
    #0: Limited area for bike sharing locaiton, 1: Full area for others
    geojson = read_geojson()
    #Inject id for mapping (somehow we need to do it after loading the geojson)
    gdf_plr = get_plr()
    if area == 1:
        for k in range(len(geojson['features'])):
            geojson['features'][k]['PLR_ID'] = gdf_plr.iloc[k, 0]

    elif area == 0:
        for k in range(len(geojson['features'])):
            n = str(gdf_plr.iloc[k, 0])[:3]
            if  n != '032' and n != '033' and n != '034' and n != '035' and n != '042'and \
                n != '051' and n != '052' and n != '053' and n != '054' and n != '062' and \
                n != '063' and n != '064' and n != '075' and n != '076' and n != '082' and \
                n != '083' and n != '084' and n != '091' and n != '092' and n != '093' and \
                n != '094' and n != '095' and n != '115' and n != '101' and n != '102' and \
                n != '103' and n != '111' and n != '112' and n != '113' and n != '114' and \
                n != '104' and n != '121' and n != '122' and n != '124' and n != '125' and n != '126':
                geojson['features'][k]['PLR_ID'] = gdf_plr.iloc[k, 0]

    else:
        return print('Failed. Please enter 0 or 1')
    return geojson
