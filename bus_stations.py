import json
import logging
import os
import requests

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
        with open("resources/bus_station_test_data.json", "r") as test_data_file:
            bus_stations = json.load(test_data_file)
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
