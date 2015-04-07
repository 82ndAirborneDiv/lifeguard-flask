from flask import Flask
from flask import request

app = Flask(__name__)

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


if __name__ == '__main__':
    app.debug = True
    app.run()
