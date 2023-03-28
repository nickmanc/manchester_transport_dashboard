import logging
import os

import requests

test_bus_station_data = {'Altrincham Interchange': {'id': 'altrincham-interchange-bus',
                                                    'href': '/public-transport/bus/stations/altrincham-interchange-bus'},
                         'Ashton-under-Lyne Interchange': {'id': 'ashton-bus',
                                                           'href': '/public-transport/bus/stations/ashton-bus'},
                         'Bolton interchange': {'id': 'bolton-interchange-bus',
                                                'href': '/public-transport/bus/stations/bolton-interchange-bus'},
                         'Bury Interchange': {'id': 'bury-interchange-bus',
                                              'href': '/public-transport/bus/stations/bury-interchange-bus'},
                         'Chorlton': {'id': 'chorlton-bus', 'href': '/public-transport/bus/stations/chorlton-bus'},
                         'Eccles Interchange': {'id': 'eccles-interchange-bus',
                                                'href': '/public-transport/bus/stations/eccles-interchange-bus'},
                         'Farnworth': {'id': 'farnworth-bus', 'href': '/public-transport/bus/stations/farnworth-bus'},
                         'Hyde': {'id': 'hyde-bus', 'href': '/public-transport/bus/stations/hyde-bus'},
                         'Leigh': {'id': 'leigh-bus', 'href': '/public-transport/bus/stations/leigh-bus'},
                         'Manchester Airport The Station': {'id': 'manchester-airport-the-station-bus',
                                                            'href': '/public-transport/bus/stations/manchester-airport-the-station-bus'},
                         'Manchester Central Coach Station': {'id': 'manchester-central-bus',
                                                              'href': '/public-transport/bus/stations/manchester-central-bus'},
                         'Manchester Piccadilly Gardens': {'id': 'manchester-piccadilly-gardens-bus',
                                                           'href': '/public-transport/bus/stations/manchester-piccadilly-gardens-bus'},
                         'Middleton': {'id': 'middleton-bus', 'href': '/public-transport/bus/stations/middleton-bus'},
                         'Oldham': {'id': 'oldham-bus', 'href': '/public-transport/bus/stations/oldham-bus'},
                         'Pendleton': {'id': 'pendleton-bus', 'href': '/public-transport/bus/stations/pendleton-bus'},
                         'Radcliffe': {'id': 'radcliffe-bus', 'href': '/public-transport/bus/stations/radcliffe-bus'},
                         'Rochdale Interchange': {'id': 'rochdale-interchange-bus',
                                                  'href': '/public-transport/bus/stations/rochdale-interchange-bus'},
                         'Shudehill Interchange': {'id': 'shudehill-interchange-bus',
                                                   'href': '/public-transport/bus/stations/shudehill-interchange-bus'},
                         'Southern Cemetery': {'id': 'southern-cemetery-bus',
                                               'href': '/public-transport/bus/stations/southern-cemetery-bus'},
                         'Stalybridge': {'id': 'stalybridge-bus',
                                         'href': '/public-transport/bus/stations/stalybridge-bus'},
                         'Stockport Heaton Lane': {'id': 'stockport-bus',
                                                   'href': '/public-transport/bus/stations/stockport-bus'},
                         'The Trafford Centre': {'id': 'the-trafford-centre-bus',
                                                 'href': '/public-transport/bus/stations/the-trafford-centre-bus'},
                         'Wigan': {'id': 'wigan-bus', 'href': '/public-transport/bus/stations/wigan-bus'},
                         'Wythenshawe Interchange': {'id': 'wythenshawe-interchange-bus',
                                                     'href': '/public-transport/bus/stations/wythenshawe-interchange-bus'}}

# this isn't an official API, but it's there :-)
api_endpoint = "https://tfgm.com/api/public-transport/stations/"
params = {
    "$format": "json"
}


def is_running_local():
    return 'running_local' in os.environ and os.environ['running_local'] == 'true'


def get_bus_stations():
    bus_stations = {}
    if is_running_local():
        bus_stations = test_bus_station_data
    else:
        try:
            response = requests.get(api_endpoint)
            if response.status_code != 200:
                logging.exception(
                    f"Exception when retrieving bus stations. Response: {response.status_code} {response.json()}")
                return None
            data = response.json()
            for station in data:
                if station["mode"] == 'bus':
                    name = station['name'].replace("bus station", "").strip()
                    bus_stations[name] = {"id": station['id'], "href": station['href']}
        except Exception:
            logging.exception('Exception when retrieving bus stations')
    return bus_stations
