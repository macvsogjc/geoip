import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

account_id = os.getenv('MAXMIND_ACCOUNT_ID')
license_key = os.getenv('MAXMIND_LICENSE_KEY')

def get_geolocations(ip_addresses):
    geolocations = []

    for ip in ip_addresses:
        response = requests.get(
            f'https://geolite.info/geoip/v2.1/city/{ip}',
            auth=HTTPBasicAuth(account_id, license_key)
        )
        if response.status_code == 200:
            data = response.json()
            geolocations.append({
                'ip': ip,
                'latitude': data['location']['latitude'],
                'longitude': data['location']['longitude'],
                'country': data['country']['iso_code']
            })

    return geolocations
