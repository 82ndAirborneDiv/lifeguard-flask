from flask import Flask, render_template
from flask import request
from datetime import datetime
from flask.ext.googlemaps import GoogleMaps
from flask.ext.googlemaps import Map
import pytz


class PersonMap:
    def __init__(self, name):
        self.name = name
        self.latitude = 0.0
        self.longitude = 0.0
        self.map_id = name + '_map'
        self.map = Map(identifier=self.map_id, lat=self.latitude,
                       lng=self.longitude, markers=[(self.latitude, self.longitude)])

    def update_location(self, lat, lon):
        self.latitude = lat
        self.longitude = lon
        self.map = Map(identifier=self.map_id, lat=self.latitude,
                       lng=self.longitude, markers=[(self.latitude, self.longitude)])


device_owners = {
    'E3F83A40-E509-4EAB-B770-CD2CAAD86A4B': 'Greg',
    'A6AF418B-B6D3-44DF-A634-7F21E42F8496': 'Jacob',
    '043E6CF8-C979-44EE-8266-644CDF93B902': 'Nick',
    'ED33EFF5-04B3-4458-A5CF-64E774540AB9': 'Pam',
    'FEA35E1F-6B61-4E33-AE9E-16855E7EF6CA': 'Tom'

}

owner_maps = {
    'Greg': PersonMap('Greg'),
    'Pam': PersonMap('Pam'),
    'Jacob': PersonMap('Jacob'),
    'Nick': PersonMap('Nick'),
    'Tom': PersonMap('Tom')
}


app = Flask(__name__)
GoogleMaps(app)
tz = pytz.timezone('America/New_York')

@app.route('/')
def home():
    return render_template('home.html', owner_maps=owner_maps)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/location', methods=['POST', 'GET'])
def location():

    device = request.args.get('p')
    # get time in tz
    posix_timestamp = request.args.get('t')
    dt = datetime.fromtimestamp(float(posix_timestamp), tz)
    latitude = request.args.get('lat')
    longitude = request.args.get('long')

    if device in device_owners:
        owner = device_owners[device]
        owner_map = owner_maps[owner]
        owner_map.update_location(latitude, longitude)
    else:
        owner = 'unknown (device: ' + device + ')'

    result = 'Lifeguard update at ' + dt.strftime('%Y-%m-%d %I:%M:%S %p') + ' for ' + owner + ': ' + latitude + ',' + longitude
    print(result)
    return result


if __name__ == '__main__':
    app.debug = True
    app.run()
