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
-----------------
How Freedge works
-----------------
  * For every 120 seconds, we collect the current temperature / humidty of the
  freedge.

  * For every 3600 seconds (1 hour),  we collect images inside the freedge 
  (for quality control analysis later).

  * Whenever someone open/close the door, we also collect data from all
  sensors, including images, temp/hudmidty, and active period.
  
  * In addition, the update interval will be reset starting from last active 
  period.

  * All collected data will send to a Cloud Database.
"""
import sys
import time
import cv2
import argparse

from Freedge import Freedge
#from cloud.CloudDB import CloudDB
#from cloud.CloudML import CloudML
from cloud.utils import parse_label_map

def main(args):
  # ############################
  # Initialize cloud and Freedge
  # ############################
  # Cloud Machine Learning Service to predict what items in Freedge.
  '''freedgeAI = CloudML(
    host='172.30.60.141',
    port=9000,
    model='faster_rcnn_inception_resnet_v2_atrous_coco',
    label_dict=parse_label_map('/home/pi/mscoco.pbtxt'))
  print('Freedge AI is intialized.')
'''
  
  # Cloud Database to store sensory data
  '''cloud = CloudDB(
      host=args.cloudb_host, 
      port=args.cloudb_port, 
      database=args.cloudb_database, 
      verbose=args.verbose)
  print('Freedge CloudDB is intialized.')
'''
  
  # Freedge Protoype Object
  freedge = Freedge(
      device_id=args.device_id,
      camera_update_interval=args.camera_update_interval,
      weather_update_interval=args.weather_update_interval,
      verbose=args.verbose)

  # ##########################
  # Main Loop
  # ##########################
  print('Freedge Prototype is intialized. \n\nStarting running...')
  try: 
    while True:
      images = freedge.run()
      #sensory_data, images = freedge.run()#CANCELLED IN THE SIMPLE VERSION
      """ #CANCELLED IN THE SIMPLE VERSION
      # Upload data to cloud
      if sensory_data:
        msg, ok = cloud.upload(sensory_data, args.device_id, location='US')
        """  
      # Perform  Object Detection on new images [for demo purposes].
      # Later, this process should be run in cloud.
      '''if images:
        for idx in images.keys():
          try:
            food_items = freedgeAI.predict(images[idx])
            image = freedgeAI.visualize(images[idx], food_items)
          except Exception as e:
            print("ML service is temporarily unavailable.")
            pass
          cv2.imwrite('/home/pi/outputs/camera%s.jpg'%idx, image)
        print('Images are updated!.\n')
      time.sleep(0.1)
       '''
  except KeyboardInterrupt as exit_signal:
    print('Ctrl + C is pressed')
    print('Shutting down...')
    freedge.shutdown()
    print('Bye!')


def parse_args():
  args = argparse.ArgumentParser()
  args.add_argument('--device_id', type=str, default='freedgePrototype')
  args.add_argument('--camera_update_interval', type=int, default=3600)
  args.add_argument('--weather_update_interval', type=int, default=120)
  args.add_argument('--cloudb_host', type=str, default='172.30.67.178')
  args.add_argument('--cloudb_port', type=int, default=8086)
  args.add_argument('--cloudb_database', type=str, default='freedgeDB')
  args.add_argument('--verbose', type=bool, default=True)
  return args.parse_args()


if __name__ == '__main__':
  args = parse_args()
  main(args)