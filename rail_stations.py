import logging
import streamlit as st
import requests
import xml.etree.ElementTree as et


def get_authentication_token():
    logging.info("Getting datafeeds.nationalrail.co.uk authentication token")
    url = "https://datafeeds.nationalrail.co.uk/authenticate"
    data = {"username": st.secrets.datafeeds.nationalrail.co.uk_credentials.username,
            "password": st.secrets.datafeeds.nationalrail.co.uk_credentials.password}
    requests.urllib3.disable_warnings()
    response = requests.post(url, data=data, verify=False)
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
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            xml = et.fromstring(response.content)
            # Define the namespace
            ns = {'n': 'http://nationalrail.co.uk/xml/station',
                  'add': 'http://www.govtalk.gov.uk/people/AddressAndPersonalDetails',
                  'com': 'http://nationalrail.co.uk/xml/common'}

            greater_manchester_postcodes = ["BL1", "BL2", "BL3", "BL4", "BL5", "BL6", "BL8", "BL9", "M1", "M11", "M12",
                                            "M13", "M14", "M15", "M16", "M17", "M18", "M19", "M2", "M20", "M21", "M22",
                                            "M23", "M24", "M25", "M26", "M27", "M28", "M29", "M3", "M30", "M31", "M32",
                                            "M33", "M34", "M35", "M38", "M4", "M40", "M41", "M43", "M44", "M45", "M46",
                                            "M5", "M50", "M6", "M7", "M8", "M9", "M90", "OL1", "OL10", "OL11", "OL15",
                                            "OL16", "OL2", "OL3", "OL4", "OL5", "OL6", "OL7", "OL8", "OL9", "SK1",
                                            "SK14", "SK15", "SK16", "SK2", "SK3", "SK4", "SK5", "SK6", "SK7", "SK8",
                                            "WA14", "WA15", "WN1", "WN2", "WN3", "WN4", "WN5", "WN6", "WN7"]
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
            logging.exception(f"Problem when retrieving rail stations, response was  {response.status_code}")
    except Exception as e:
        logging.exception('Exception when retrieving rail stations')
    return gm_stations
