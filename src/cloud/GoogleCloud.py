#!/usr/bin/env python

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Python sample for connecting to Google Cloud IoT Core via MQTT, using JWT.
***Deprecated***
****Notes***:
 This one provides scable solution, however, it seems to be too 
complicated for this project.
"""

# [START iot_mqtt_includes]
import argparse
import datetime
import os
import random
import ssl
import time

import jwt
import paho.mqtt.client as mqt
# [END iot_mqtt_includes]


class GoogleIoT(object):
  """Google Cloud IoT Core API. This one provides scable solution, however,
  it seems to be too complicated for this project.
  
  Example usage:
  --------------
    iot_cloud = GoogleIoT(
        project_id=args.project_id,
        cloud_region=args.location,
        registry_id=args.registry_id,
        device_id=args.device_id, 
        mqtt_bridge_hostname='mqtt.googleapis.com',
        mqtt_bridge_port='443', 
        ca_certs=args.ca_certs, 
        private_key_file=args.private_key, 
        algorithm=args.encryption_algorithm,
        token_renew_period=60)
    iot_cloud.connect()
  """
  def __init__(self, 
               project_id, 
               cloud_region, 
               registry_id, 
               device_id,
               mqtt_bridge_hostname, 
               mqtt_bridge_port, 
               ca_certs, 
               private_key_file, 
               algorithm,
               token_renew_period):
    
    self.project_id = project_id
    self.cloud_region = cloud_region
    self.registry_id = registry_id
    self.device_id = device_id

    self.mqtt_bridge_hostname = mqtt_bridge_hostname
    self.mqtt_bridge_port = mqtt_bridge_port

    self.ca_certs = ca_certs 
    self.private_key_file = private_key_file
    self.algorithm = algorithm
               
    self.client = None
    self.token_issued_date = 0
    self.token_renew_period = token_renew_period

  def is_jwt_expired(self):
    seconds_since_issue = (datetime.datetime.utcnow() - self.token_issued_date).seconds
    if seconds_since_issue > 60 * self.token_renew_period:
      return True
    else:
      return False
      
  def connect(self):
    # Generate a MQTT Broker to deliver/recive messages 
    self.client = get_client(
        self.project_id, 
        self.cloud_region, 
        self.registry_id, 
        self. device_id, 
        self.private_key_file, 
        self.algorithm, 
        self.ca_certs, 
        self.mqtt_bridge_hostname, 
        self.mqtt_bridge_port)
    self.token_issued_date = datetime.datetime.now()
    # Start listening to MQTT message
    self.client.loop()

  def publish(self, topic, data):
    if self.is_jwt_expired():
      self.connect()
    else:
      mqtt_topic = '/devices/{}/{}'.format(self.device_id, topic)
      payload = json.dumps(data)
      print('Publishing message  {}'.format(payload))
      self.client.publish(mqtt_topic, payload, qos=1)


# [START iot_mqtt_jwt]
def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
        Args:
         project_id: The cloud project ID this device belongs to
         private_key_file: A path to a file containing either an RSA256 or
                 ES256 private key.
         algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
        Returns:
            An MQTT generated from the given project_id and private key, which
            expires in 20 minutes. After 20 minutes, your client will be
            disconnected, and a new JWT will have to be generated.
        Raises:
            ValueError: If the private_key_file does not contain a known key.
        """

    token = {
            # The time that the token was issued at
            'iat': datetime.datetime.utcnow(),
            # The time the token expires.
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            # The audience field should always be set to the GCP project id.
            'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
            algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)
# [END iot_mqtt_jwt]


# [START iot_mqtt_config]
def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print('on_connect', mqtt.connack_string(rc))


def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print('on_disconnect', error_str(rc))


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print('on_publish')


def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = str(message.payload)
    print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, message.topic, str(message.qos)))


def get_client(
        project_id, cloud_region, registry_id, device_id, private_key_file,
        algorithm, ca_certs, mqtt_bridge_hostname, mqtt_bridge_port):
    """Create our MQTT client. The client_id is a unique string that identifies
    this device. For Google Cloud IoT Core, it must be in the format below."""
    client = mqtt.Client(
            client_id=('projects/{}/locations/{}/registries/{}/devices/{}'
                       .format(
                               project_id,
                               cloud_region,
                               registry_id,
                               device_id)))

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
            username='unused',
            password=create_jwt(
                    project_id, private_key_file, algorithm))

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Register message callbacks. https://eclipse.org/paho/clients/python/docs/
    # describes additional callbacks that Paho supports. In this example, the
    # callbacks just print to standard out.
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to the Google MQTT bridge.
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    # This is the topic that the device will receive configuration updates on.
    mqtt_config_topic = '/devices/{}/config'.format(device_id)

    # Subscribe to the config topic.
    client.subscribe(mqtt_config_topic, qos=1)

    return client
# [END iot_mqtt_config]


