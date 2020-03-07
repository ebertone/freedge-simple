# MIT License

# Copyright (c) 2018 Freedge.org

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =============================================================================
'''
import os
import cv2

class Camera(object):
    def __init__(self, device=0, output_path='/home/pi/outputs', **kwargs):
        self.device = device
        super(Camera,self).__init__(**kwargs)

    def takes_photo(self, output_path):
        print("\nTaking photo from camera %s"% self.device)
        cap = cv2.VideoCapture(self.device)

        # Set settings manually
        # Reference: Python 2.4.9
        # https://docs.opencv.org/2.4.9/modules/highgui/doc/reading_and_writing_images_and_video.html?highlight=videocapture#videocapture-set
        cap.set(3,640)  # CV_CAP_PROP_FRAME_WIDTH
        cap.set(4,480)  # CV_CAP_PROP_FRAME_HEIGHT
        ret, image = cap.read()
        if not ret:
            print('Cannot read camera %s' % self.device)
            cap.release()
            return None
        # Hack: flip upside down
        image = cv2.flip(image, -1)
        img_file = os.path.join(output_path, 'camera%s.jpg' % self.device)
        cv2.imwrite(img_file, image)
        cap.release()
        return image
'''
#This works

import os
import cv2
output_path='/home/pi/outputs'
cap=cv2.VideoCapture(0)
cap.set(3,640)  # CV_CAP_PROP_FRAME_WIDTH
cap.set(4,480)  # CV_CAP_PROP_FRAME_HEIGHT
ret, image = cap.read() #cap.read is reading two things and the image is the second one
img_file = os.path.join(output_path, 'camera_test.jpg' )
print (img_file)
cv2.imwrite(img_file, image)
