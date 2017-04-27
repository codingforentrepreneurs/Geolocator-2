import datetime
from decimal import Decimal
import requests
from django.conf import settings

from django.utils import timezone


YELP_AUTH_ENDPOINT = 'https://api.yelp.com/oauth2/token'
YELP_SEARCH_ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
YELP_CLIENT_ID = getattr(settings, 'YELP_CLIENT_ID', 'ZWcWfw0GR2iFNbSVrZtxyg')
YELP_CLIENT_SECRET = getattr(settings, 'YELP_CLIENT_SECRET','TATGfe5b9QUcd2ckuDxWUGH8f7YkDUeRe7cWlnYbwXNppOM8hdyhnTYSYakQCAKz')

def timestamp_in_past(timestamp_string):
    now = timezone.now() #python datetime
    timestamp_dec = Decimal(timestamp_string) # int("123") / float(123.123)
    timestamp_unaware = datetime.datetime.fromtimestamp(timestamp_dec)
    current_tz = timezone.get_current_timezone()
    timestamp_aware = timezone.make_aware(timestamp_unaware, current_tz)
    if timestamp_aware < now:
        return True # in the past
    return False # not in the past

def get_token(request=None):
    token_exists = False
    token = None
    if request:
        session_token = request.session.get('YELP_TOKEN')
        token_expires = request.session.get('YELP_EXPIRES')
        if session_token and token_expires:
            expired = timestamp_in_past(token_expires)
            if not expired:
                token_exists = True
                token = session_token
    if not token_exists:
        params = {
            'grant_type': 'OAUTH2',
            'client_id': YELP_CLIENT_ID,
            'client_secret': YELP_CLIENT_SECRET
        }
        r = requests.post(YELP_AUTH_ENDPOINT, params=params)
        token = r.json()['access_token']
        expires = r.json()['expires_in'] #seconds
        if request:
            request.session['YELP_TOKEN'] = token
            expires_in = (timezone.now() + datetime.timedelta(seconds=expires))
            expires_in_tstamp = expires_in.timestamp()
            request.session['YELP_EXPIRES'] = str(expires_in_tstamp)
            request.session.set_expiry(expires - datetime.timedelta(days=1).seconds)
    return token


def yelp_search(keyword='Food', location='Newport Beach', request=None):
    token = get_token(request=request)
    headers = {"Authorization": "Bearer " + token}
    params = {'term': keyword, 'location': location}
    r = requests.get(YELP_SEARCH_ENDPOINT, headers=headers, params=params)
    # print(r.status_code)
    return r.json()


