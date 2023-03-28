import logging

import requests

# this isn't an official API, but it's there :-)
api_endpoint = "https://tfgm.com/api/statuses/tram"
params = {
    "$format": "json"
}

def get_metrolink_line_status():
    lines = []
    try:
        response = requests.get(api_endpoint)
        if response.status_code != 200:
            logging.exception(f"ERROR Line Status: {response.status_code} {response.json()}")
            return None
        data = response.json()
        for line in data['items']:
            lines.append({"name": line.get("name"), "status": line.get("status"), "severity": line.get("severity"),
                          "details": line.get("detail")})

    except Exception:
        logging.exception('Exception when retrieving metrolink line status')
    return lines
