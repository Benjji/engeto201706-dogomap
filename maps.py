from folium import Map, FeatureGroup, Marker, Icon, RegularPolygonMarker, GeoJson, LayerControl, CircleMarker
from json import loads
import codecs
import requests


def get_long_lat(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyAZdptvPWWMO060tQpmbN_GKCZFjcCZzEY'.format(
        address.replace(' ', '+'))
    response = requests.get(url)
    payload = response.json()
    if payload['results']:
        payload = payload['results'][0]['geometry']['location']
        return payload['lat'], payload['lng']


def get_dict_from_josn(file_name):
    return loads(codecs.open(file_name, 'r', encoding='utf-8', errors='ignore').read())


def mark_on_map(dog, dogos):
    if not (dog.get('-col_6', False) and dog.get('-col_5', False) and dog.get('-col_4', False)):
        return
    dog_location = get_long_lat('{-col_6} {-col_5}, {-col_4}'.format(**dog))
    dogos.add_child(RegularPolygonMarker(location=dog_location, fill_color='red' if dog[
                    '-col_3'] == 'Ano' else 'blue', popup=dog['-col_0'], number_of_sides=8, radius=10))
    # If dogo is aggressive
    if dog['-col_3'] == 'Ano':
        CircleMarker(location=dog_location, radius=25,  popup=dog['-col_0'],
                     color='#A63740', fill_color='red').add_to(dogos)


map = Map(location=get_long_lat('Presov'), zoom_start=13)

dogos = FeatureGroup(name='Dogos')
dogos_file = get_dict_from_josn('psy.json')

c = 0
for dog in dogos_file['ds']['rs']['data']['row']:
    if c > 70:
        break
    c += 1
    mark_on_map(dog, dogos)

map.add_child(dogos)
map.add_child(LayerControl())
map.save('maps.html')
