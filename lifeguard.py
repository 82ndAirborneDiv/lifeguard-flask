from flask import Flask, render_template
from flask import request
from datetime import datetime
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import pytz


app = Flask(__name__)
GoogleMaps(app)
tz = pytz.timezone('America/New_York')


# Waldo APIs
devices = {}


@app.route('/')
def home():
    return render_template('home.html', devices=devices)


@app.route('/about')
def about():
    return render_template('about.html')


class UserMap:
    def __init__(self, name):
        self.name = name
        self.latitude = 42.4343779
        self.longitude = -83.9891627
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


class Device:
    def __init__(self, device_id, user_id, name):
        self.device_id = device_id
        self.name = name
        self.user_id = user_id
        self.map = UserMap(name)

    def update_device(self, user_id, name):
        self.user_id = user_id
        self.name = name


@app.route('/devicecheckin', methods=['POST'])
def device_check_in():
    checkin_data = request.get_json()

    device_id = checkin_data['id']
    lat = checkin_data['lat']
    lng = checkin_data['lng']
    time = checkin_data['time']
    #mode = checkin_data['mode']
    dt = datetime.fromtimestamp(float(time), tz)

    result = "Waldo device check in API result: "

    if device_id in devices:
        device = devices[device_id]
        map = device.map
        map.update_location(lat, lng, dt)
        result = result + "updating device {} with location (lat,ln) ({},{}) at {}.".format(device_id, lat, lng, dt)
    else:
        result = result + "error due to unknown device."
    return result


@app.route('/registration', methods=['POST'])
def device_registration():
    registration_data = request.get_json()

    device_id = registration_data['deviceId']
    user_id = registration_data['userId']
    name = registration_data['name']

    result = "Waldo user registration API result: "

    if device_id in devices:
        devices[device_id].update_device(user_id, name)
        result = result + "updating device {} with user name {} with user ID of {}.".format(device_id, name, user_id)
    else:
        device = Device(device_id, user_id, name)
        devices[device_id] = device
        result = result + "adding device {} for user name {} with user ID of {}.".format(device_id, name, user_id)

    return result


if __name__ == '__main__':
    app.debug = True
    app.run()
