from flask import Flask, render_template
from flask import request
from datetime import datetime
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import pytz


class PersonMap:
    def __init__(self, name):
        self.name = name
        self.latitude = 0.0
        self.longitude = 0.0
        self.map_id = name + '_map'
        self.map = Map(identifier=self.map_id, lat=self.latitude,
                       lng=self.longitude, markers=[(self.latitude, self.longitude)])
        self.last_update = None

    def update_location(self, lat, lon, dt=None):
        self.latitude = lat
        self.longitude = lon
        self.map = Map(identifier=self.map_id, lat=self.latitude,
                       lng=self.longitude, markers=[(self.latitude, self.longitude)])
        self.last_update = dt


device_owners = {
    '0529CF2B-AEBD-4E81-8DD0-A99DDCC4EA60': 'Greg',

}

owner_maps = {
    'Greg': PersonMap('Greg L.'),
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
    longitude = request.args.get('lng')

    if device in device_owners:
        owner = device_owners[device]
        owner_map = owner_maps[owner]
        owner_map.update_location(latitude, longitude, dt)
    else:
        owner = 'unknown (device: ' + device + ')'

    result = 'Lifeguard location updated at ' + dt.strftime('%Y-%m-%d %I:%M:%S %p') + ' for ' + owner + ': ' + latitude + ',' + longitude
    print(result)
    return result


@app.route('/register', methods=['POST', 'GET'])
def register_user():

    device = request.args.get('p')
    # get time in tz
    posix_timestamp = request.args.get('t')
    dt = datetime.fromtimestamp(float(posix_timestamp), tz)
    user_id = request.args.get('uid')
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')

    if device in device_owners:
        owner_maps[device_owners[device]].update_location(latitude, longitude, dt)
    else:
        owner_maps[user_id] = PersonMap(user_id)
        owner_maps[user_id].update_location(latitude, longitude, dt)
        device_owners[device] = user_id

    result = 'Lifeguard user registered with user name ' + user_id
    print(result)
    return result


@app.route('/visit', methods=['POST', 'GET'])
def visit():

    user = request.args.get('user')
    # get time in tz
    timestamp = request.args.get('t')

    latitude = request.args.get('lat')
    longitude = request.args.get('lng')
    arrive = request.args.get('arrive')
    depart = request.args.get('depart')

    if user in owner_maps:
        owner_map = owner_maps[user]
        owner_map.update_location(latitude, longitude)
    else:
        user = 'Unknown user: ' + user

    result = 'Lifeguard visit update at ' + timestamp + ' for ' + user + ': ' + ' arrived at ' + arrive + \
             ', departed at ' + depart + ', at location ' + latitude + ',' + longitude

    print(result)
    return result


# Waldo APIs
@app.route('/devicecheckin', methods=['POST'])
def device_check_in():
    checkin_data = request.get_json()

    device_id = checkin_data['id']
    lat = checkin_data['lat']
    lng = checkin_data['lng']
    time = checkin_data['time']
    mode = checkin_data['mode']


if __name__ == '__main__':
    app.debug = True
    app.run()
