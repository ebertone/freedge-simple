# MIT License
#
# Copyright (c) 2018 Freedge.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =============================================================================
"""
Reference: 
[1] https://influxdb-python.readthedocs.io/en/latest/api-documentation.html
"""
import json
import requests
import influxdb
from datetime import datetime


class CloudDB(object):

  def __init__(self, host, port, database, verbose=True):
    self.verbose = verbose
    self.database = database
    self.client = influxdb.InfluxDBClient(host=host, port=port,database=database)

  def upload(self, data, device_id, location):
    # Time format : "2018-06-05T23:00:00Z",
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    messages = []
    status = None

    # Parse Data into Standard InfluxDB format
    for measurement in data.keys():
      msg = {
        "time": current_time,
        "measurement": measurement,
        "tags":{
          "device": device_id,
          "location": location},
        "fields": data[measurement]}
      messages.append(msg)

    # Send data to cloud
    try:
      status = self.client.write_points(messages)
      if self.verbose:
        print('Uploading new updates to cloud..')
        print('Status: %s' %status)
        print('Message: {}'.format(messages))

    except influxdb.exceptions.InfluxDBClientError as database_error:
      print(database_error)
      print("Creating database")
      self.client.create_database(self.database)

    finally:
      return messages, status
