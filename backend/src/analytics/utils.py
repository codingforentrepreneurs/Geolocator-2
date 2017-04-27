from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2

GEO_DEFAULT_IP = getattr(settings, 'GEO_DEFAULT_IP', '72.14.207.99')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for is not None:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    ip_address = ip or GEO_DEFAULT_IP
    if str(ip_address) == '127.0.0.1':
        ip_address = GEO_DEFAULT_IP
    return ip_address


def get_client_city_data(ip_address):
    g = GeoIP2()
    try:
        return g.city(ip_address)
    except:
        return None