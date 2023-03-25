from zeep import Client, Settings, xsd
from zeep.plugins import HistoryPlugin
import logging
import streamlit as st

LDB_TOKEN = st.secrets.lite.realtime.nationalrail.co.uk_credentials.open.ldbws.token
WSDL = 'http://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2021-11-01'

settings = Settings(strict=False)
history = HistoryPlugin()
client = Client(wsdl=WSDL, settings=settings, plugins=[history])

header = xsd.Element(
    '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken',
    xsd.ComplexType([
        xsd.Element(
            '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}TokenValue',
            xsd.String()),
    ])
)
header_value = header(TokenValue=LDB_TOKEN)


def get_train_departures(station_code):
    departures = []
    try:
        station_board = client.service.GetDepartureBoard(numRows=10, crs=station_code, _soapheaders=[header_value])
        services = station_board.trainServices.service
        for service in services:
            departures.append({"due": service.std, "expected": "" if service.etd == 'On time' else service.etd,
                               "destination": service.destination.location[0].locationName, "platform": service.platform})
    except Exception:
        logging.exception('Exception when retrieving departures')
    return departures

def get_train_arrivals(station_code):
    arrivals = []
    try:
        station_board = client.service.GetArrivalBoard(numRows=10, crs=station_code, _soapheaders=[header_value])
        services = station_board.trainServices.service
        for service in services:
            arrivals.append({"due": service.sta, "expected": "" if service.eta == 'On time' else service.eta,
                               "destination": service.origin.location[0].locationName, "platform": service.platform})
    except Exception:
        logging.exception('Exception when retrieving arrivals')
    return arrivals


