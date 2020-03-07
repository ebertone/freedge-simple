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
"""Camera Manager allows program to control activate multiple cameras
at the same time.
"""
from .Camera import Camera

class CameraMananger(object):
    def __init__(self, devices, id):
        self.id = id
        self.activated = False
        self.manager = self._setup(devices)

    def activate(self):
        print("hi")
        self.activated = True

    def is_activated(self):
        return self.activated

    def trigger(self, output_path='/home/pi/'):
        self.activated = False
        images = {}
        for cam in self.manager:
            image = cam.takes_photo(output_path)
            if image is not None:
                images[cam.id] = image
        return images

    def _setup(self, devices):
        manager = []
        device_id, _ = self.id.split('_')
        for idx, device in enumerate(devices):
            camera = Camera(
                device=device, 
                id='{}_camera_{}'.format(device_id, idx))
            manager.append(camera)
        return manager