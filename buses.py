import logging
import requests
import re
import streamlit as st
from bs4 import BeautifulSoup

@st.cache_data(ttl=10, show_spinner=False)
def get_bus_departures(station):
    #no api for this I can find so scraping the website
    url = f"https://tfgm.com/public-transport/bus/stations/{station}"
    departures = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        departure_rows = soup.find_all('tr', id=re.compile("departure-\\d*"))
        for departure_row in departure_rows:
            departure_destination_block = departure_row.find('td', {'class': 'departure-destination'})
            bus_number = departure_destination_block.h3.text
            bus_operator = departure_row.find('td', {'class': 'departure-operator'}).text
            bus_stand = departure_row.find('td', {'class': 'departure-stand'}).text
            live = departure_row.find('span', {'class': 'departure-indicator'}).text.strip()[0] == 'L'
            destination = departure_destination_block.p.text
            expected_departure = departure_row.find('td', {'class': 'departure-expected'}).span.text
            departures.append({"destination": destination, "expected": expected_departure, "stand": bus_stand,
                               "live": live, "number": bus_number, "operator": bus_operator})
    except Exception:
        logging.exception('Exception when retrieving buses')
    logging.info(f"bus departures for {station}: {departures}")
    return departures
