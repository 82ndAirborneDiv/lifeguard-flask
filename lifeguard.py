from flask import Flask
from flask import request

app = Flask(__name__)
device_owners = {
    'BFFE2480-0A6A-485A-8056-8EA2FDF3EFC4': 'Greg Ledbetter',
    '9D2A19B1-4E04-4BAA-87F4-13C0A8DACC97': 'Jacob Ledbetter',
    '77A9E170-4A56-4A8A-9E01-370128A3CD02': 'Nick Ledbetter',
    '5C4FB776-FC26-45CA-B9AC-F0B89F7E1D36': 'iPhone 6 Simulator'

}
@app.route('/')
def hello_world():
    return 'Hello from Lifeguard location server!\n'

@app.route('/location', methods=['POST', 'GET'])
def location():
    device = request.args.get('p')
    timestamp = request.args.get('t')
    lat = request.args.get('lat')
    long = request.args.get('long')
    print('Received Location update: Timestamp = ' + timestamp + ' Latitude = ' + lat + ' Longitude = ' + long + ' Device ID ' + device)
    return 'Date time stamp = ' + timestamp + ' Latitude = ' + lat + ' Longitude = ' + long + ' Device ID ' + device + '\n'


def get_user(device_id):
    return device_owners[device_id]


if __name__ == '__main__':
    app.debug = True
    app.run()
