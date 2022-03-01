import requests
import datetime
import os
import psycopg2
import psycopg2.extras
import config
import logging
import pandas as pd
import csv
import time

def get_nextbike_locations ():

    # request data
    URL = "https://gbfs.nextbike.net/maps/gbfs/v1/nextbike_bn/en/free_bike_status.json"

    # sending get request and saving the response as response object
    response = requests.get(url = URL)
    try:
        r = response.json()
        nextbikes = []
        for i in range(len(r['data']['bikes'])):
            try:
                bike_id = int(r['data']['bikes'][i]['bike_id'])
            except:
                # single bike have no ID (?!); skip these bikes
                continue

            lat = r['data']['bikes'][i]['lat']
            lon = r['data']['bikes'][i]['lon']
            nextbikes.append([bike_id, query_date, lat,lon])
        return nextbikes
    except Exception:
        logging.exception("message")


def get_lidlbike_locations():

    #Berlin lat lon
    radius_center_lat=52.520008
    radius_center_lon=13.404954

    # request data
    URL = "https://api.deutschebahn.com/flinkster-api-ng/v1/bookingproposals"

    radius=10000 # radius in meter, max 10000 (10km)
    providernetwork=2
    expand='rentalObject'
    limit = 50

    offset = 0 # scroll with offset through pagination
    more_bikes = True
    key = config.key1

    lidlbikes = []
    while more_bikes:
        try:

            #header
            # note in header
            headers = {"Authorization": key, "Accept": "application/json"}

            # defining a params dict for the parameters to be sent to the API
            PARAMS = {'lat':radius_center_lat, 'lon':radius_center_lon, 'radius':radius, 'providernetwork':providernetwork, 'expand':expand,
            'limit':limit, 'offset':offset}

            # sending get request and saving the response as response object
            response = requests.get(url = URL, params = PARAMS, headers=headers)

            r = response.json()

            # if bad response without items then skip
            if ('items' in r):
                for i in range(len(r['items'])):
                    bike_id = r['items'][i]['rentalObject']['providerRentalObjectId']

                    # single bike have no ID (?!); skip these bikes
                    if not bike_id:
                        continue

                    lat = r['items'][i]['position']['coordinates'][1]
                    lon = r['items'][i]['position']['coordinates'][0]
                    lidlbikes.append([bike_id, LIDLBIKE, query_date, lat, lon])

                # get all paginations
                offset += 50
                if len(r['items']) < 50:
                    more_bikes = False

                # 30 calls max per minute (then timeout)
                if (offset % 3000 == 0):
                    key = config.key3
                elif (offset % 1500 == 0):
                    key = config.key2

            else:
                more_bikes = False


        except Exception:
            more_bikes = False
            logging.exception("message")

    return lidlbikes

def get_mobike_locations():

    # request data
    URL = "http://app.mobike.com/api/nearby/v4/nearbyBikeInfo"
    plattform= '1'

    # header
    headers = {"plattform": plattform, \
        "Content-Type": "application/x-www-form-urlencoded", \
        "User-Agent" : "Mozilla/5.0 (Android 7.1.2; Pixel Build/NHG47Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.9 NTENTBrowser/3.7.0.496 (IWireless-US) Mobile Safari/537.36"}

    radius_centers = pd.read_csv("coordinates.csv")

    mobikes = []
    for i in range (radius_centers.shape[0]):
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'latitude': radius_centers.iloc[i, 0], 'longitude': radius_centers.iloc[i, 1]}

        # sending get request and saving the response as response object
        response = requests.get(url = URL, params = PARAMS, headers = headers)

        #Todo error handling
        try:
            r = response.json()

            # if no error is returned, get bike information
            if r['code'] == 0:

                for i in range(len(r['bike'])):
                    bike_id = r['bike'][i]['distId'][1:]
                    lat = r['bike'][i]['distY']
                    lon = r['bike'][i]['distX']
                    mobikes.append([bike_id, MOBIKE, query_date, lat, lon])

            else:
                continue

        except Exception:
            logging.exception("message")

    return mobikes

if __name__== "__main__":

    while 1 > 0:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        logging.basicConfig(level=logging.INFO, filename="logfile.log")
        logger = logging.getLogger(__name__)

        # Connect to an existing database
        query_date = datetime.datetime.now()
        NEXTBIKE = 0
        LIDLBIKE = 1
        MOBIKE = 2

        nextbikes = get_nextbike_locations()
        #Save in csv
        nextbikes = pd.DataFrame(nextbikes)
        time_stamp = time.strftime("%m%d_%H%M")
        nextbikes.to_csv(f'data/livedata_{time_stamp}.csv', index=False)
        time.sleep(60*10)

#    lidlbikes = get_lidlbike_locations()


    #mobikes = get_mobike_locations()


    # insert into database
#    conn = psycopg2.connect("host=" + config.dbhost + " dbname=" + config.dbname + " user=" + config.dbuser + " password=" + config.dbpassword)

#    cur = conn.cursor()
#    sql = """INSERT INTO public."bikeLocations"("id", "bikeId", "providerId", "timestamp", latitude, longitude) VALUES %s ON CONFLICT DO NOTHING"""
#    psycopg2.extras.execute_values(cur, sql, nextbikes, template='(DEFAULT, %s, %s, %s, %s, %s)')
#    psycopg2.extras.execute_values(cur, sql, lidlbikes, template='(DEFAULT, %s, %s, %s, %s, %s)')
#   psycopg2.extras.execute_values(cur, sql, mobikes, template='(DEFAULT, %s, %s, %s, %s, %s)')

#    conn.commit()
#    cur.close()
#    conn.close()
