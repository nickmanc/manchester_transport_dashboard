import json
import logging
import os

import requests
import xml.etree.ElementTree as et

with open("resources/greater_manchester_postcodes.json", 'r') as postcode_file:
    greater_manchester_postcodes = json.load(postcode_file)
def is_running_local():
    return 'running_local' in os.environ and os.environ['running_local'] == 'true'


def get_authentication_token():
    logging.info("Getting datafeeds.nationalrail.co.uk authentication token")
    url = "https://datafeeds.nationalrail.co.uk/authenticate"
    data = {"username": os.environ["datafeeds_nationalrail_co_uk_username"],
            "password": os.environ["datafeeds_nationalrail_co_uk_password"]}
    requests.urllib3.disable_warnings()
    response = requests.post(url, data=data, verify=False)
    token = None
    if response.status_code == 200:
        response_json = response.json()
        token = response_json['token']
    else:
        logging.exception("Error:", response.status_code, response.text)
    return token


def get_rail_stations():
    url = "http://opendata.nationalrail.co.uk/api/staticfeeds/4.0/stations"
    headers = {
        "Content-Type": "application/xml",
        "X-Auth-Token": get_authentication_token()
    }
    gm_stations = {}

    if is_running_local():
        with open("resources/train_station_test_data.json", "r") as test_data_file:
            gm_stations = json.load(test_data_file)
    else:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                xml = et.fromstring(response.content)
                # Define the namespace
                ns = {'n': 'http://nationalrail.co.uk/xml/station',
                      'add': 'http://www.govtalk.gov.uk/people/AddressAndPersonalDetails',
                      'com': 'http://nationalrail.co.uk/xml/common'}
                # Loop over each station element and extract the name and CRS code
                for station in xml.findall('n:Station', ns):
                    address = station.find('n:Address', ns)
                    if address is not None:
                        postal_address = address.find('com:PostalAddress', ns)
                        if postal_address is not None:
                            five_line_postal_address = postal_address.find('add:A_5LineAddress', ns)
                            if five_line_postal_address is not None:
                                postcode = five_line_postal_address.find('add:PostCode', ns)
                                if postcode is not None:
                                    for greater_manchester_postcode in greater_manchester_postcodes:
                                        # if postcode starts with greater_manchester_postcode then add to stations
                                        if postcode.text.startswith(greater_manchester_postcode):
                                            name = station.find('n:Name', ns).text
                                            crscode = station.find('n:CrsCode', ns).text
                                            gm_stations[name] = crscode
            else:
                logging.error(f"Problem when retrieving rail stations, response was  {response.status_code}")
        except Exception:
            logging.error('Exception when retrieving rail stations')
    return gm_stations
