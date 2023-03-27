import os

import pytz
import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

from bus_stations import get_bus_stations
from rail_stations import get_rail_stations
from trams import get_tram_stations
from trams import get_tram_departures
from trains import get_train_departures, get_train_arrivals
from buses import get_bus_departures
from metrolink_lines import get_metrolink_line_status

st.set_page_config(layout="wide")
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


@st.cache_data(ttl=60 * 60 * 24)
def get_cached_list_of_tram_stops():
    return get_tram_stations()


@st.cache_data(ttl=60 * 60 * 24)
def get_cached_rail_stations():
    return get_rail_stations()


@st.cache_data(ttl=60 * 60 * 24)
def get_cached_bus_stations():
    return get_bus_stations()


presets = {"Altrincham": {"Title":"Altrincham", "Metrolink":"Altrincham", "Rail":"Altrincham", "Bus":"Altrincham Interchange"},
           "Piccadilly": {"Title":"Manchester Piccadilly", "Metrolink":"Piccadilly", "Rail":"Manchester Piccadilly", "Bus":"Manchester Piccadilly Gardens"},
           "Ashton": {"Title":"Ashton", "Metrolink":"Ashton-Under-Lyne", "Rail":"Ashton-under-Lyne", "Bus":"Ashton-under-Lyne Interchange"},
           "Airport": {"Title":"Manchester Airport", "Metrolink":"Manchester Airport", "Rail":"Manchester Airport", "Bus":"Manchester Airport The Station"},
           "Custom":{"Title":"Manchester", "Metrolink":"Piccadilly", "Rail":"Manchester Piccadilly", "Bus":"Manchester Piccadilly Gardens"}}

# st_autorefresh(interval=60 * 1000)
st_autorefresh(interval=20 * 1000)
with st.sidebar:
    selectedPreset = st.radio("Select a preset", presets.keys())
    # st.session_state['selectedPreset'] = st.radio("Select a preset", presets.keys())
    selected_dashboard_title = st.text_input("Dashboard title", f"{presets[selectedPreset]['Title']} Transport Dashboard", disabled=selectedPreset!='Custom')

    tram_stops = get_cached_list_of_tram_stops()
    tram_stop_names = sorted(list(tram_stops.keys()))
    default_index = tram_stop_names.index(presets[selectedPreset]['Metrolink'])
    selected_tram_stop_name = st.selectbox(
        'Select a metrolink stop', (tram_stop_names), index=default_index, disabled=selectedPreset!='Custom')
    tram_stop_ids = tram_stops[selected_tram_stop_name]["location_ids"]

    rail_stations = get_cached_rail_stations()
    rail_station_names = sorted(list(rail_stations.keys()))
    default_index = rail_station_names.index(presets[selectedPreset]['Rail'])
    selected_train_station_name = st.selectbox('Select a train station', rail_station_names, index=default_index, disabled=selectedPreset!='Custom')
    show_arrivals = st.checkbox('Show arrivals', disabled=selectedPreset!='Custom')

    bus_stations = get_cached_bus_stations()
    bus_station_names = sorted(list(bus_stations.keys()))
    default_index = bus_station_names.index(presets[selectedPreset]['Bus'])
    selected_bus_station_name = st.selectbox('Select a bus station', bus_station_names, index=default_index, disabled=selectedPreset!='Custom')

titleCol1, titleCol2 = st.columns([5, 1])
titleCol1.title(selected_dashboard_title)
manchester_tz = pytz.timezone('Europe/London')
current_manchester_time = datetime.now().astimezone(manchester_tz)
titleCol2.title(current_manchester_time.strftime("%H:%M"))

col1, col2, col3 = st.columns(3)
# Display tram information in a table
col1.subheader(
    f"[Metrolink ({selected_tram_stop_name})](https://tfgm.com{tram_stops[selected_tram_stop_name]['href']})")
tramDepartureInfo = get_tram_departures(tram_stop_ids)
trams = tramDepartureInfo[0]
if len(trams) > 0:
    for tram in trams:
        if tram['expected'] == 0:
            tramExpectedText = "NOW"
        else:
            tramExpectedText = f"in **{tram['expected']}** minutes."
        col1.markdown(f"**{tram['destination']}**  ({tram['carriages']}) **{tramExpectedText}**")
else:
    col1.markdown("No trams currently scheduled to depart.")
tramMessage = '**``' + tramDepartureInfo[1] + '``**'
# tramMessage = '**``' + tramDepartureInfo[1].replace("^F0","").replace("^J","") + '``**'
col1.markdown(tramMessage)
col1.subheader("[Metrolink Status](https://tfgm.com/live-updates)")
metrolinkLineStatuses = get_metrolink_line_status()
if len(metrolinkLineStatuses) > 0:
    for metrolinkLineStatus in metrolinkLineStatuses:
        if metrolinkLineStatus.get('severity') == 'danger':
            statusColour = "red"
        elif metrolinkLineStatus.get('severity') == 'warning':
            statusColour = "orange"
        else:
            statusColour = "green"

        col1.markdown(f"**{metrolinkLineStatus['name']}** - :{statusColour}[🛈 {metrolinkLineStatus['status']}]")
else:
    col1.write("No line status available.")

col2.subheader(
    f"[Rail({selected_train_station_name})](https://ojp.nationalrail.co.uk/service/ldbboard/dep/{rail_stations[selected_train_station_name]})")
col2.subheader("Departures")
trains = get_train_departures(rail_stations[selected_train_station_name])
if len(trains) > 0:
    for train in trains:
        trainMessage = f"**{train['due']}**  **:red[{train['expected']}]** **{train['destination']}**"
        if train['expected'] != 'Cancelled':
            trainMessage = trainMessage + f" - Platform {train['platform']}"
        col2.write(trainMessage)
else:
    col2.write("No trains currently scheduled to depart.")

if show_arrivals:
    col2.subheader("Arrivals")
    trains = get_train_arrivals(rail_stations[selected_train_station_name])
    if len(trains) > 0:
        for train in trains:
            trainMessage = f"**{train['due']}**  **:red[{train['expected']}]** **{train['destination']}**"
            if train['expected'] != 'Cancelled':
                trainMessage = trainMessage + f" - Platform {train['platform']}"
            col2.write(trainMessage)
    else:
        col2.write("No trains currently scheduled to arrive.")

col3.subheader(
    f"[Bus ({selected_bus_station_name})](https://tfgm.com{bus_stations[selected_bus_station_name]['href']})")
buses = get_bus_departures(bus_stations[selected_bus_station_name]['id'])
if len(buses) > 0:
    for bus in buses:
        departureTimeText = f"**NOW**" if "Due" == bus['expected'] else f"at **{bus['expected']}**" if ":" in bus[
            'expected'] else f"in **{bus['expected']} minutes**"
        if not (bus['live']):  departureTimeText += "*"
        col3.write(
            f"**{bus['number']}** - **{bus['destination']}** - Stand {bus['stand']} {departureTimeText}")
        # f"**{bus['number']}** ({bus['operator']}) **{bus['destination']}** - Stand {bus['stand']} {departureTimeText}")
else:
    col3.write("No buses currently scheduled to depart.")

col1, col2, col3 = st.columns(3)
col3.write("                         _* timetabled_")

footer = f"""<style>
  .footer {{
    display: flex; /* display the elements in a row */
    justify-content: space-between; /* space the elements evenly */
    align-items: center; /* center the items vertically */
    padding: 10px 0; /* add some padding to the top and bottom */
    width: 100%; /* set the width to 100% */
    color: grey;
    justify-content: space-around;
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
      <td>Version: {os.getenv("DASHBOARD_BUILD_VERSION","local")}</td>
    </tr>
  </table>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
