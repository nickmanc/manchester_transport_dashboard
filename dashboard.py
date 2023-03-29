import json
import logging
import os
import pytz
import streamlit as st
from datetime import datetime

from streamlit_autorefresh import st_autorefresh
from streamlit_cookies_manager import CookieManager

from bus_stations import get_bus_stations
from rail_stations import get_rail_stations
from trams import get_tram_stations
from trams import get_tram_departures
from trains import get_train_departures, get_train_arrivals
from buses import get_bus_departures
from metrolink_lines import get_metrolink_line_status

SELECTED_BUS_STATION_KEY = "selected_bus_station"

SELECTED_RAIL_STATION_KEY = "selected_rail_station"

SELECTED_TRAM_STOP_KEY = "selected_tram_stop"

DASHBOARD_TITLE_KEY = "dashboard_title_key"

SELECTED_PRESET_KEY = "selected_preset"

DASHBOARD_DATA_KEY = "mtd-data-v0.0.1"


@st.cache_data(ttl=60 * 60 * 24)
def get_cached_list_of_tram_stops():
    return get_tram_stations()


@st.cache_data(ttl=60 * 60 * 24)
def get_cached_rail_stations():
    return get_rail_stations()


@st.cache_data(ttl=60 * 60 * 24)
def get_cached_bus_stations():
    return get_bus_stations()


@st.cache_data
def load_presets():
    with open("resources/presets.json", "r+") as presets_file:
        return json.load(presets_file)


@st.cache_data
def configure_logging():
    # get the log level from the environment variable
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    # create logger object
    logger = logging.getLogger()
    # set log level based on environment variable
    logger.setLevel(getattr(logging, log_level.upper()))
    # create console handler with custom format
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)
    # add console handler to logger
    logger.removeHandler(logger.handlers[0])  # must be better way of doing this but remove default handler
    logger.addHandler(console_handler)


def save_user_settings():
    logging.info("Saving user settings")
    cookies[DASHBOARD_DATA_KEY] = json.dumps(
        {DASHBOARD_TITLE_KEY: st.session_state.dashboard_title,
         SELECTED_TRAM_STOP_KEY: st.session_state.selected_tram_stop,
         SELECTED_RAIL_STATION_KEY: st.session_state.selected_rail_station,
         SELECTED_BUS_STATION_KEY: st.session_state.selected_bus_station,
         SELECTED_PRESET_KEY: st.session_state.preset_key})
    cookies.save()


def get_value_from_cookie_or_default(key, default):
    if DASHBOARD_DATA_KEY not in cookies or cookies[DASHBOARD_DATA_KEY] is None:
        return default
    cookie = json.loads(cookies[DASHBOARD_DATA_KEY])
    if key not in cookie:
        return default
    else:
        return cookie[key]


def apply_preset():
    preset = presets[st.session_state.preset_key]
    st.session_state.dashboard_title = preset["Title"]
    st.session_state.selected_tram_stop = preset["Metrolink"]
    st.session_state.selected_rail_station = preset["Rail"]
    st.session_state.selected_bus_station = preset["Bus"]

# this needs to be called before any other streamlit code
st.set_page_config(page_title="Manchester Transport Dashboard", page_icon=':railway_car:', layout="wide")
        # ,menu_items={
        # 'Report a Bug': "mailto: bug@manchester-transport.co.uk",
        # 'About': "This is a free application that pulls together data from sources such as [National Rail Enquiries](https://nationalrail.co.uk)  and [Transport for Greater Manchester](https://tfgm.com) to provide a single dashboard for transport in Manchester."})
st_autorefresh(interval=10 * 1000)
# cookies = EncryptedCookieManager(
cookies = CookieManager( #TODO - switch to encrypted cookies
    prefix="nickmanc/manchester-transport-dashboard/"
    # You should really setup a long cookies_password secret if you're running on Streamlit Cloud.
    # password=os.environ.get("cookies_password", "default password")
)
if not cookies.ready():
    # Wait for the component to load and send us current cookies.
    st.stop()

# get rid of massive blank header
st.markdown(
    """
        <style>
            .appview-container .main .block-container {{
                padding-top: {padding_top}rem;
                padding-bottom: {padding_bottom}rem;
                }}

        </style>""".format(
        padding_top=0, padding_bottom=1
    ),
    unsafe_allow_html=True,
)

configure_logging()
presets = load_presets()

default_selection = presets['Custom']
selected_preset_key = get_value_from_cookie_or_default(SELECTED_PRESET_KEY, 'Custom')
selected_dashboard_title = get_value_from_cookie_or_default(DASHBOARD_TITLE_KEY, default_selection['Title'])
selected_tram_stop_name = get_value_from_cookie_or_default(SELECTED_TRAM_STOP_KEY, default_selection['Metrolink'])
selected_train_station_name = get_value_from_cookie_or_default(SELECTED_RAIL_STATION_KEY, default_selection['Rail'])
selected_bus_station_name = get_value_from_cookie_or_default(SELECTED_BUS_STATION_KEY, default_selection['Bus'])

manchester_tz = pytz.timezone('Europe/London')
current_manchester_time = datetime.now().astimezone(manchester_tz)

with st.sidebar:
    preset_options = list(presets.keys())
    selected_index = preset_options.index(selected_preset_key)
    selectedPreset = st.radio("Select a preset, or customise your own dashboard", preset_options, index=selected_index,
                              key='preset_key', on_change=apply_preset)
    disable_fields = selectedPreset != 'Custom'
    with st.form(key='dashboard_form'):
        selected_dashboard_title = st.text_input("Dashboard Title", f"{selected_dashboard_title}",
                                                 key="dashboard_title", disabled=disable_fields)

        tram_stops = get_cached_list_of_tram_stops()
        tram_stop_names = sorted(list(tram_stops.keys()))
        selected_tram_stop_name_index = tram_stop_names.index(selected_tram_stop_name)
        selected_tram_stop_name = st.selectbox(
            'Select a Metrolink stop', tram_stop_names, index=selected_tram_stop_name_index, key="selected_tram_stop",
            disabled=disable_fields)
        tram_stop_ids = tram_stops[selected_tram_stop_name]["location_ids"]

        rail_stations = get_cached_rail_stations()
        rail_station_names = sorted(list(rail_stations.keys()))
        selected_rail_station_name_index = rail_station_names.index(selected_train_station_name)
        selected_train_station_name = st.selectbox('Select a train station', rail_station_names,
                                                   index=selected_rail_station_name_index, key="selected_rail_station",
                                                   disabled=disable_fields)
        show_arrivals = st.checkbox('Show arrivals', disabled=disable_fields)

        bus_stations = get_cached_bus_stations()
        bus_station_names = sorted(list(bus_stations.keys()))
        selected_bus_station_name_index = bus_station_names.index(selected_bus_station_name)
        selected_bus_station_name = st.selectbox('Select a bus station', bus_station_names,
                                                 index=selected_bus_station_name_index,
                                                 key="selected_bus_station", disabled=disable_fields)
        submit_button = st.form_submit_button(label='Save', on_click=save_user_settings)

titleCol1, titleCol2 = st.columns([5, 1])
titleCol1.title(selected_dashboard_title)
titleCol2.title(current_manchester_time.strftime("%H:%M"))

tram_column, rail_column, bus_column = st.columns(3)
tram_column.subheader(
    f"[Metrolink ({selected_tram_stop_name})](https://tfgm.com{tram_stops[selected_tram_stop_name]['href']})")
tramDepartureInfo = get_tram_departures(tram_stop_ids)
trams = tramDepartureInfo[0]
if len(trams) > 0:
    for tram in trams:
        if tram['expected'] == 0:
            tramExpectedText = "NOW"
        else:
            tramExpectedText = f"in **{tram['expected']}** minutes."
        tram_column.markdown(f"**{tram['destination']}**  ({tram['carriages']}) **{tramExpectedText}**")
else:
    tram_column.markdown("No trams currently scheduled to depart.")
tramMessage = '**``' + tramDepartureInfo[1] + '``**'
tram_column.markdown(tramMessage)
tram_column.subheader("[Metrolink Status](https://tfgm.com/live-updates)")

metrolinkLineStatuses = get_metrolink_line_status()
if len(metrolinkLineStatuses) > 0:
    for metrolinkLineStatus in metrolinkLineStatuses:
        if metrolinkLineStatus.get('severity') == 'danger':
            statusColour = "red"
        elif metrolinkLineStatus.get('severity') == 'warning':
            statusColour = "orange"
        else:
            statusColour = "green"

        tram_column.markdown(f"**{metrolinkLineStatus['name']}** - :{statusColour}[🛈 {metrolinkLineStatus['status']}]")
else:
    tram_column.write("No line status available")

rail_column.subheader(
    f"[Rail({selected_train_station_name})](https://ojp.nationalrail.co.uk/service/ldbboard/dep/"
    f"{rail_stations[selected_train_station_name]})")
rail_column.subheader("Departures")
trains = get_train_departures(rail_stations[selected_train_station_name])
if len(trains) > 0:
    for train in trains:
        trainMessage = f"**{train['due']}**  **:red[{train['expected']}]** **{train['destination']}**"
        if train['expected'] != 'Cancelled':
            trainMessage = trainMessage + f" - Platform {train['platform']}"
        rail_column.write(trainMessage)
else:
    rail_column.write("No trains currently scheduled to depart")

if show_arrivals:
    rail_column.subheader("Arrivals")
    trains = get_train_arrivals(rail_stations[selected_train_station_name])
    if len(trains) > 0:
        for train in trains:
            trainMessage = f"**{train['due']}**  **:red[{train['expected']}]** **{train['destination']}**"
            if train['expected'] != 'Cancelled':
                trainMessage = trainMessage + f" - Platform {train['platform']}"
            rail_column.write(trainMessage)
    else:
        rail_column.write("No trains currently scheduled to arrive")

bus_column.subheader(
    f"[Bus ({selected_bus_station_name})](https://tfgm.com{bus_stations[selected_bus_station_name]['href']})")
buses = get_bus_departures(bus_stations[selected_bus_station_name]['id'])
if len(buses) > 0:
    for bus in buses:
        if "Due" == bus['expected']:
            departureTimeText = "**NOW**"
        elif ":" in bus['expected']:
            departureTimeText = f"at **{bus['expected']}**"
        else:
            departureTimeText = f"in **{bus['expected']} minutes**"
        if not (bus['live']):  departureTimeText += "*"
        bus_column.write(
            f"**{bus['number']}** - **{bus['destination']}** - Stand {bus['stand']} {departureTimeText}")
else:
    bus_column.write("No buses currently scheduled to depart")

tram_column, rail_column, bus_column = st.columns(3)
bus_column.write("                         _* timetabled_")

footer = f"""<style>
    
   footer {{visibility: hidden;}}
   #MainMenu {{visibility: hidden;}}
  .content-wrapper {{
    min-height: 100vh; /* set min-height to 100% viewport height */
    position: relative; /* add position relative for child positioning */
  }}
  .footer {{
    display: flex; /* display the elements in a row */
    justify-content: space-between; /* space the elements evenly */
    align-items: center; /* center the items vertically */
    padding: 10px 0; /* add some padding to the top and bottom */
    width: 100%; /* set the width to 100% */
    color: grey;
    justify-content: space-around;
  }}

  .footer table {{
    # position: absolute; 
    bottom: 0; /* position the element at the bottom of the page */
  }}
  .footer td {{
    border: none; /* remove the borders from the table cells */
  }}
</style>
<div class="footer">
  <table>
    <tr>
      <td>Last updated: {current_manchester_time.strftime('%H:%M:%S')}</td>
      <td>Powered by National Rail Enquiries.</td>
      <td>Contains Transport for Greater Manchester data</td>
      <td>Made with <a href="https://streamlit.io">Streamlit</a></td>
      <td>Version: {os.getenv("DASHBOARD_BUILD_VERSION", "local")}</td>
    </tr>
  </table>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
