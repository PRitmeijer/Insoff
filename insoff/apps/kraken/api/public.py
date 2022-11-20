import hashlib
import requests
import time
import urllib.parse
import hmac
import base64
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def kraken_request_public(path):
    url = settings.KRAKEN_BASE_URL + settings.KRAKEN_PUBLIC_PATH + path
    response = requests.get(url)
    return response

def get_ohlc_data(pair, interval, since):
    url = f'OHLC?pair={pair}&interval={interval}&since={since}'
    response = kraken_request_public(url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        logger.error(f'Could not retrieve OHLC data for URL: {response.url}')
        return