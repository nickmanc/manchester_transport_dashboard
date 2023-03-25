import logging

import requests

# this isn't an official API, but it's there :-)
api_endpoint = "https://tfgm.com/api/public-transport/stations/"
params = {
    "$format": "json"
}


def get_bus_stations():
    bus_stations = {}
    try:
        response = requests.get(api_endpoint)
        if response.status_code != 200:
            logging.exception(f"Exception when retrieving bus stations. Response: {response.status_code} {response.json()}")
            return None
        data = response.json()
        for station in data:
            if station["mode"] == 'bus':
                bus_stations[station['name']] = {"id": station['id'], "href": station['href']}
    except Exception:
        logging.exception('Exception when retrieving bus stations')
    return bus_stations
