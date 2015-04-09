from flask import Flask
from flask import request
from datetime import datetime

import pytz

app = Flask(__name__)
device_owners = {
    'BFFE2480-0A6A-485A-8056-8EA2FDF3EFC4': 'Greg Ledbetter',
    'A6AF418B-B6D3-44DF-A634-7F21E42F8496': 'Jacob Ledbetter',
    '043E6CF8-C979-44EE-8266-644CDF93B902': 'Nick Ledbetter',
    'ED33EFF5-04B3-4458-A5CF-64E774540AB9': 'Pam Ledbetter'

}
tz = pytz.timezone('America/New_York')


@app.route('/')
def hello_world():
    return 'Hello from Lifeguard location server!\n'

@app.route('/location', methods=['POST', 'GET'])
def location():
    device = request.args.get('p')

    if device in device_owners:
        owner = device_owners[device]
    else:
        owner = 'Unknown owner for device: ' + device

    # get time in tz
    posix_timestamp = request.args.get('t')
    dt = datetime.fromtimestamp(float(posix_timestamp), tz)

    latitude = request.args.get('lat')
    longitude = request.args.get('long')

    result = 'Received Location update: Time = ' + dt.strftime('%Y-%m-%d %I:%M:%S %p') + ' Latitude = ' + latitude + ' Longitude = ' + longitude + ' Person =  ' + owner
    print(result)
    return result



if __name__ == '__main__':
    app.debug = False
    app.run()
