### Getting a list of staions

use

to get api token need to register at https://opendata.nationalrail.co.uk/ and then get your token by making call to
authenticate endpoint:

    curl -k --data-urlencode "username=nXXXXXXX@hotmail.com" --data-urlencode "password=XXXXXXXXXXX" 
    https://datafeeds.nationalrail.co.uk/authenticate
