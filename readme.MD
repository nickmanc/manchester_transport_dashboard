### Runtime arguments
running_local=true  # this will skip the loading of station data which otherwise takes a few seconds on application startup.

;LOG_LEVEL=WARN


### running with docker compose

    docker-compose up --build

### Required API Keys
You'll need to get a API keys for the services this application uses.  For local use these can be stored in a file .streamlit/secrets.toml using this template

    #datafeeds.nationalrail.co.uk_credentials
    datafeeds_nationalrail_co_uk_username=
    datafeeds_nationalrail_co_uk_password=
    
    #lite.realtime.nationalrail.co.uk_credentials
    open_ldbws_token=
    
    #tfgm credentials
    api_tfgm_com_key=

Make them available as environment variables if you want to use them in a docker container

You can register for keys using the following links:

TFGM: https://developer.tfgm.com/
Open LDBWS: https://lite.realtime.nationalrail.co.uk/OpenLDBWSRegistration/
datafeeds.nationalrail.co.uk: https://opendata.nationalrail.co.uk/

### Getting a list of stations

use

to get api token need to register at https://opendata.nationalrail.co.uk/ and then get your token by making call to
authenticate endpoint:

    curl -k --data-urlencode "username=nXXXXXXX@hotmail.com" --data-urlencode "password=XXXXXXXXXXX" 
    https://datafeeds.nationalrail.co.uk/authenticate

### API Limits
developer.tfgm.com - 2000 calls/minute
OpenLDBWS - Usage is capped at 5000 requests / hour
opendata.nationalrail.co.uk - not sure, but just using this to get station list on startup so should be fine
