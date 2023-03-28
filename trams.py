import os
import requests
import streamlit as st
import logging

test_tram_stop_data = {'Abraham Moss': {'location_ids': [15648, 15649], 'href': '/public-transport/tram/stops/abraham-moss-tram'}, 'Altrincham': {'location_ids': [15621, 15622], 'href': '/public-transport/tram/stops/altrincham-tram'}, 'Anchorage': {'location_ids': [15709, 15710], 'href': '/public-transport/tram/stops/anchorage-tram'}, 'Ashton Moss': {'location_ids': [15681, 15682], 'href': '/public-transport/tram/stops/ashton-moss-tram'}, 'Ashton West': {'location_ids': [15683, 15684], 'href': '/public-transport/tram/stops/ashton-west-tram'}, 'Ashton-Under-Lyne': {'location_ids': [15677, 15678, 15679, 15680], 'href': '/public-transport/tram/stops/ashton-under-lyne-tram'}, 'Audenshaw': {'location_ids': [15685, 15686], 'href': '/public-transport/tram/stops/audenshaw-tram'}, 'Baguley': {'location_ids': [15590, 15591], 'href': '/public-transport/tram/stops/baguley-tram'}, 'Barlow Moor Road': {'location_ids': [15594, 15595], 'href': '/public-transport/tram/stops/barlow-moor-road-tram'}, 'Barton Dock Road': {'location_ids': [15807, 15808], 'href': '/public-transport/tram/stops/barton-dock-road-tram'}, 'Benchill': {'location_ids': [15592, 15593], 'href': '/public-transport/tram/stops/benchill-tram'}, 'Besses O Th Barn': {'location_ids': [15652, 15653], 'href': '/public-transport/tram/stops/besses-o-th-barn-tram'}, 'Bowker Vale': {'location_ids': [15650, 15651], 'href': '/public-transport/tram/stops/bowker-vale-tram'}, 'Broadway': {'location_ids': [15711, 15712], 'href': '/public-transport/tram/stops/broadway-tram'}, 'Brooklands': {'location_ids': [15623, 15624], 'href': '/public-transport/tram/stops/brooklands-tram'}, 'Burton Road': {'location_ids': [15789, 15790], 'href': '/public-transport/tram/stops/burton-road-tram'}, 'Bury': {'location_ids': [15654, 15655], 'href': '/public-transport/tram/stops/bury-tram'}, 'Cemetery Road': {'location_ids': [15687, 15688], 'href': '/public-transport/tram/stops/cemetery-road-tram'}, 'Central Park': {'location_ids': [15744, 15745], 'href': '/public-transport/tram/stops/central-park-tram'}, 'Chorlton': {'location_ids': [15791, 15792], 'href': '/public-transport/tram/stops/chorlton-tram'}, 'Clayton Hall': {'location_ids': [15689, 15690, 15691], 'href': '/public-transport/tram/stops/clayton-hall-tram'}, 'Cornbrook': {'location_ids': [15713, 15714, 15715, 15716], 'href': '/public-transport/tram/stops/cornbrook-tram'}, 'Crossacres': {'location_ids': [15596, 15597], 'href': '/public-transport/tram/stops/crossacres-tram'}, 'Crumpsall': {'location_ids': [15656, 15657, 15658], 'href': '/public-transport/tram/stops/crumpsall-tram'}, 'Dane Road': {'location_ids': [15625, 15626], 'href': '/public-transport/tram/stops/dane-road-tram'}, 'Deansgate - Castlefield': {'location_ids': [15627, 15628, 15629], 'href': '/public-transport/tram/stops/deansgate-castlefield-tram'}, 'Derker': {'location_ids': [15746, 15747], 'href': '/public-transport/tram/stops/derker-tram'}, 'Didsbury Village': {'location_ids': [15793, 15794], 'href': '/public-transport/tram/stops/didsbury-village-tram'}, 'Droylsden': {'location_ids': [15692, 15693], 'href': '/public-transport/tram/stops/droylsden-tram'}, 'East Didsbury': {'location_ids': [15795, 15796, 15797, 15798], 'href': '/public-transport/tram/stops/east-didsbury-tram'}, 'Eccles': {'location_ids': [15717], 'href': '/public-transport/tram/stops/eccles-tram'}, 'Edge Lane': {'location_ids': [15694, 15695, 15696, 15697], 'href': '/public-transport/tram/stops/edge-lane-tram'}, 'Etihad Campus': {'location_ids': [15702, 15703, 15704, 15705], 'href': '/public-transport/tram/stops/etihad-campus-tram'}, 'Exchange Quay': {'location_ids': [15718, 15719], 'href': '/public-transport/tram/stops/exchange-quay-tram'}, 'Exchange Square': {'location_ids': [15720, 15721], 'href': '/public-transport/tram/stops/exchange-square-tram'}, 'Failsworth': {'location_ids': [15748, 15749], 'href': '/public-transport/tram/stops/failsworth-tram'}, 'Firswood': {'location_ids': [15799, 15800], 'href': '/public-transport/tram/stops/firswood-tram'}, 'Freehold': {'location_ids': [15750, 15751], 'href': '/public-transport/tram/stops/freehold-tram'}, 'Harbour City': {'location_ids': [15722, 15723], 'href': '/public-transport/tram/stops/harbour-city-tram'}, 'Heaton Park': {'location_ids': [15659, 15660], 'href': '/public-transport/tram/stops/heaton-park-tram'}, 'Hollinwood': {'location_ids': [15752, 15753], 'href': '/public-transport/tram/stops/hollinwood-tram'}, 'Holt Town': {'location_ids': [15698, 15699], 'href': '/public-transport/tram/stops/holt-town-tram'}, 'Imperial War Museum': {'location_ids': [15809, 15810], 'href': '/public-transport/tram/stops/imperial-war-museum-tram'}, 'Kingsway Business Park': {'location_ids': [15754, 15755], 'href': '/public-transport/tram/stops/kingsway-business-park-tram'}, 'Ladywell': {'location_ids': [15724, 15725], 'href': '/public-transport/tram/stops/ladywell-tram'}, 'Langworthy': {'location_ids': [15726, 15727], 'href': '/public-transport/tram/stops/langworthy-tram'}, 'Manchester Airport': {'location_ids': [15588, 15589], 'href': '/public-transport/tram/stops/manchester-airport-tram'}, 'Market Street': {'location_ids': [15661, 15662], 'href': '/public-transport/tram/stops/market-street-tram'}, 'Martinscroft': {'location_ids': [15598, 15599], 'href': '/public-transport/tram/stops/martinscroft-tram'}, 'MediaCityUK': {'location_ids': [15728, 15729, 15730, 15731], 'href': '/public-transport/tram/stops/mediacityuk-tram'}, 'Milnrow': {'location_ids': [15756, 15757], 'href': '/public-transport/tram/stops/milnrow-tram'}, 'Monsall': {'location_ids': [15758, 15759], 'href': '/public-transport/tram/stops/monsall-tram'}, 'Moor Road': {'location_ids': [15600, 15601], 'href': '/public-transport/tram/stops/barlow-moor-road-tram'}, 'Navigation Road': {'location_ids': [15630, 15631], 'href': '/public-transport/tram/stops/navigation-road-tram'}, 'New Islington': {'location_ids': [15700, 15701], 'href': '/public-transport/tram/stops/new-islington-tram'}, 'Newbold': {'location_ids': [15760, 15761], 'href': '/public-transport/tram/stops/newbold-tram'}, 'Newhey': {'location_ids': [15762, 15763], 'href': '/public-transport/tram/stops/newhey-tram'}, 'Newton Heath and Moston': {'location_ids': [15764, 15765], 'href': '/public-transport/tram/stops/newton-heath-and-moston-tram'}, 'Northern Moor': {'location_ids': [15602, 15603], 'href': '/public-transport/tram/stops/northern-moor-tram'}, 'Old Trafford': {'location_ids': [15632, 15633], 'href': '/public-transport/tram/stops/old-trafford-tram'}, 'Oldham Central': {'location_ids': [15766, 15767, 15768, 15769], 'href': '/public-transport/tram/stops/oldham-central-tram'}, 'Oldham King Street': {'location_ids': [15770, 15771], 'href': '/public-transport/tram/stops/oldham-king-street-tram'}, 'Oldham Mumps': {'location_ids': [15772, 15773], 'href': '/public-transport/tram/stops/oldham-mumps-tram'}, 'Parkway': {'location_ids': [15811, 15812], 'href': '/public-transport/tram/stops/parkway-tram'}, 'Peel Hall': {'location_ids': [15604, 15605], 'href': '/public-transport/tram/stops/peel-hall-tram'}, 'Piccadilly': {'location_ids': [15667, 15668], 'href': '/public-transport/tram/stops/piccadilly-gardens-tram'}, 'Piccadilly Gardens': {'location_ids': [15663, 15664, 15665, 15666], 'href': '/public-transport/tram/stops/piccadilly-gardens-tram'}, 'Pomona': {'location_ids': [15732, 15733], 'href': '/public-transport/tram/stops/pomona-tram'}, 'Prestwich': {'location_ids': [15669, 15670], 'href': '/public-transport/tram/stops/prestwich-tram'}, 'Queens Road': {'location_ids': [15671, 15672], 'href': '/public-transport/tram/stops/queens-road-tram'}, 'Radcliffe': {'location_ids': [15673, 15674], 'href': '/public-transport/tram/stops/radcliffe-tram'}, 'Robinswood Road': {'location_ids': [15606, 15607], 'href': '/public-transport/tram/stops/robinswood-road-tram'}, 'Rochdale Railway Station': {'location_ids': [15774, 15775, 15776, 15777], 'href': '/public-transport/tram/stops/rochdale-railway-station-tram'}, 'Rochdale Town Centre': {'location_ids': [15778, 15779, 15780, 15781], 'href': '/public-transport/tram/stops/rochdale-town-centre-tram'}, 'Roundthorn': {'location_ids': [15608, 15609, 15610, 15611], 'href': '/public-transport/tram/stops/roundthorn-tram'}, 'Sale': {'location_ids': [15634, 15635], 'href': '/public-transport/tram/stops/sale-tram'}, 'Sale Water Park': {'location_ids': [15614, 15615], 'href': '/public-transport/tram/stops/sale-water-park-tram'}, 'Salford Quays': {'location_ids': [15734, 15735], 'href': '/public-transport/tram/stops/salford-quays-tram'}, 'Shadowmoss': {'location_ids': [15612, 15613], 'href': '/public-transport/tram/stops/shadowmoss-tram'}, 'Shaw and Crompton': {'location_ids': [15782, 15783, 15784], 'href': '/public-transport/tram/stops/shaw-and-crompton-tram'}, 'Shudehill': {'location_ids': [15636, 15637], 'href': '/public-transport/tram/stops/shudehill-tram'}, 'South Chadderton': {'location_ids': [15785, 15786], 'href': '/public-transport/tram/stops/south-chadderton-tram'}, 'St Peters Square': {'location_ids': [15736, 15737, 15738, 15739, 15740, 15741], 'href': '/public-transport/tram/stops/st-peters-square-tram'}, 'St Werburghs Road': {'location_ids': [15801, 15802], 'href': '/public-transport/tram/stops/st-werburghs-road-tram'}, 'Stretford': {'location_ids': [15638, 15639], 'href': '/public-transport/tram/stops/stretford-tram'}, 'The Trafford Centre': {'location_ids': [15813, 15814], 'href': '/public-transport/tram/stops/the-trafford-centre-tram'}, 'Timperley': {'location_ids': [15642, 15643], 'href': '/public-transport/tram/stops/timperley-tram'}, 'Trafford Bar': {'location_ids': [15640, 15641], 'href': '/public-transport/tram/stops/trafford-bar-tram'}, 'Velopark': {'location_ids': [15706, 15707, 15708], 'href': '/public-transport/tram/stops/velopark-tram'}, 'Victoria': {'location_ids': [15644, 15645, 15646, 15647], 'href': '/public-transport/tram/stops/victoria-tram'}, 'Village': {'location_ids': [15815, 15816], 'href': '/public-transport/tram/stops/village-tram'}, 'Weaste': {'location_ids': [15742, 15743], 'href': '/public-transport/tram/stops/weaste-tram'}, 'West Didsbury': {'location_ids': [15803, 15804], 'href': '/public-transport/tram/stops/west-didsbury-tram'}, 'Westwood': {'location_ids': [15787, 15788], 'href': '/public-transport/tram/stops/westwood-tram'}, 'Wharfside': {'location_ids': [15817, 15818], 'href': '/public-transport/tram/stops/wharfside-tram'}, 'Whitefield': {'location_ids': [15675, 15676], 'href': '/public-transport/tram/stops/whitefield-tram'}, 'Withington': {'location_ids': [15805, 15806], 'href': '/public-transport/tram/stops/withington-tram'}, 'Wythenshawe Park': {'location_ids': [15616, 15617], 'href': '/public-transport/tram/stops/wythenshawe-park-tram'}, 'Wythenshawe Town Centre': {'location_ids': [15618, 15619, 15620], 'href': '/public-transport/tram/stops/wythenshawe-town-centre-tram'}}

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
        station_map = test_tram_stop_data
    else:
        api_endpoint = f"https://api.tfgm.com/odata/Metrolinks"
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


@st.cache_data(ttl=10)
def get_tram_departures(met_stop_ids):
    trams = {}
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
