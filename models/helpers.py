import requests

def get_coord(local):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': local, 'key':'AIzaSyAbB3ZXUFg39DMOtLyke5dzk5y8_WoEByE'}
    r = requests.get(url, params=params)
    results = r.json()['results']
    location = results[0]['geometry']['location']
    return [location['lat'], location['lng']]