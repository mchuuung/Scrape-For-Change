import json
import requests


global_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=10'
CMC_PRO_API_KEY = '8d477e5a-885f-4378-82eb-8a7a97541b2e'


headers = {
 'Accept': 'application/json',
 'Accept-Encoding': 'deflate, gzip',
 'X-CMC_PRO_API_KEY': CMC_PRO_API_KEY,

}

request = requests.get(global_url, headers=headers) # Gets the global url and puts the json data inside the variable 'request'
results = request.json()

print(json.dumps(results, sort_keys=True, indent=4)) # readable format

