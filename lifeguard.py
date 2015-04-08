from flask import Flask
from flask import request
from datetime import datetime

import pytz

app = Flask(__name__)
device_owners = {
    'BFFE2480-0A6A-485A-8056-8EA2FDF3EFC4': 'Greg Ledbetter',
    '9D2A19B1-4E04-4BAA-87F4-13C0A8DACC97': 'Jacob Ledbetter',
    '77A9E170-4A56-4A8A-9E01-370128A3CD02': 'Nick Ledbetter',
    '5C4FB776-FC26-45CA-B9AC-F0B89F7E1D36': 'iPhone 6 Simulator'

}
tz = pytz.timezone('America/New_York')


@app.route('/')
def hello_world():
    return 'Hello from Lifeguard location server!\n'

@app.route('/location', methods=['POST', 'GET'])
def location():
    device = request.args.get('p')
    owner = device_owners[device]

    # get time in tz
    posix_timestamp = request.args.get('t')
    dt = datetime.fromtimestamp(posix_timestamp, tz)

    latitude = request.args.get('lat')
    longitude = request.args.get('long')

    result = 'Received Location update: Time = ' + dt.strftime('%Y-%m-%d %H:%M:%S %Z%z') + ' Latitude = ' + latitude + ' Longitude = ' + longitude + ' Person =  ' + owner
    print(result)
    return result


if __name__ == '__main__':
    app.debug = True
    app.run()
