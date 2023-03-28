import json
import os
import requests
import streamlit as st
import logging

# TfGM API endpoint and parameters
api_endpoint = "https://api.tfgm.com/odata/Metrolinks(15621)"
params = {
    "$format": "json"
}
headers = {"Ocp-Apim-Subscription-Key": os.environ["api_tfgm_com_key"]}


def is_running_local():
    return 'running_local' in os.environ and os.environ['running_local'] == 'true'


def get_tram_stop_additional_info_href(stop_name):
    url = f"https://tfgm.com/api/search?type=tram-stop-gm&q={stop_name}"
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        logging.exception(f"ERROR Failed to get additional tram stop info: {response.status_code} {response.json()}" )
        return None
    data = response.json()
    return data["items"][0]['href']


def get_tram_stations():
    station_map = {}
    if is_running_local():
        with open("resources/tram_stop_test_data.json", "r") as test_data_file:
            station_map = json.load(test_data_file)
    else:
        api_endpoint = "https://api.tfgm.com/odata/Metrolinks"
        try:
            # Parse JSON response
            response = requests.get(api_endpoint, params=params, headers=headers)
            if response.status_code != 200:
                logging.exception(f"ERROR Tram Stations: {response.status_code} {response.json()}" )
                return None
            data = response.json()
            for station in sorted(data["value"], key=lambda x: x["StationLocation"]):
                name = station["StationLocation"]
                location_id = station["Id"]
                if name not in station_map:
                    additional_info_href = get_tram_stop_additional_info_href(name)
                    station_map[name] = {"location_ids":[location_id], "href": additional_info_href}
                else:
                    station_map[name]["location_ids"].append(location_id)
        except Exception:
            logging.exception('Exception when retrieving tram stations')
        logging.info("retrieved tram stations")
    return station_map


@st.cache_data(ttl=10, show_spinner=False)
def get_tram_departures(met_stop_ids):
    trams = {}
    unique_trams = {}
    message = ""
    for id in met_stop_ids:
        api_endpoint = f"https://api.tfgm.com/odata/Metrolinks({id})"
        try:
            # Parse JSON response
            response = requests.get(api_endpoint, params=params, headers=headers)
            if response.status_code != 200:
                logging.exception(f"ERROR Trams: {response.status_code} {response.json()}" )
                return None
            data = response.json()
            for i in [0,1,2]:
                if data[f"Dest{i}"] != "":
                    destination = data.get(f"Dest{i}")
                    expected = data.get(f"Wait{i}")
                    carriages = data.get(f"Carriages{i}")
                    trams[expected+destination+carriages] = ({"expected": int(expected), "destination": destination, "carriages": carriages}) #use map to unique trams
            unique_trams = list(trams.values())
            unique_trams.sort(key=lambda x: x["expected"])
            if data["MessageBoard"] != "" and data["MessageBoard"] != '<no message>':
                message = data["MessageBoard"]
        except Exception:
            logging.exception('Exception when retrieving trams')
    logging.info(f"tram departures for {met_stop_ids}: {unique_trams}, with message: {message}")
    return unique_trams, message
