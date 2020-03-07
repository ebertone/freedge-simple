"""Tensorflow Serving Client

This file is handling sending/retreiving messages from Machine Learning Cloud
"""
from __future__ import absolute_import
from __future__ import print_function


import time
import cv2
import datetime
import numpy as np
import tensorflow as tf

# TensorFlow serving python API to send messages to server
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

from .utils import draw_boxes

class CloudML(object):
  """This object is responsible for:

    * Encode image and send request to a Machine Learning Server in the Cloud
    * Interpret the result and send back to whoever calls it
  """

  def __init__(self, host, port, model, label_dict, verbose=False):
    self.host = host
    self.port = port
    self.model = model
    self.label_dict = label_dict
    self.verbose = verbose

    channel = implementations.insecure_channel(self.host, int(self.port))
    self.stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

  def predict(self, image, img_dtype=tf.uint8, timeout=20.0):

    image = np.expand_dims(image, axis=0)
    request = predict_pb2.PredictRequest()
    request.inputs['inputs'].CopyFrom(tf.make_tensor_proto(
        image,
        dtype=img_dtype))
    request.model_spec.name = self.model
    request.model_spec.signature_name = 'predict_images'

    start = time.time()
    result = self.stub.Predict(request, timeout)  # 20 secs timeout
    num_detections = int(result.outputs['num_detections'].float_val[0])

    classes = result.outputs['detection_classes'].float_val[:num_detections]
    scores = result.outputs['detection_scores'].float_val[:num_detections]
    boxes = result.outputs['detection_boxes'].float_val[:num_detections * 4]
    classes = [self.label_dict[int(idx)] if idx in self.label_dict.keys() else 'UnlabeledItem' for idx in classes ]
    boxes = [boxes[i:i + 4] for i in range(0, len(boxes), 4)]

    if self.verbose:
        print("Number of detections: %s" % len(classes))
        print("Server Prediction in {:.3f} ms".format(
            1000*(time.time() - start)))
    return boxes, classes, scores

  def visualize(self, image, detections):
    bboxes, classes, scores = detections
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Put time stamp text on image
    cv2.putText(
      image, 
      datetime.datetime.now().strftime("%d %B %Y %I:%M:%S%p"),
      (image.shape[0] - 40, image.shape[0] - 20), 
      cv2.FONT_HERSHEY_SIMPLEX, 
      0.4, (255, 255, 255), 1)

    image = draw_boxes(image, bboxes, classes, scores)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    return image
