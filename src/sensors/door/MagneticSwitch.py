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
import time
import datetime
import RPi.GPIO as GPIO
from ..Sensor import Sensor

# Magnetic Switch runs in BCM mode
GPIO.setmode(GPIO.BCM)

class MagneticSwitch(Sensor):
    def __init__(self, pin, **kwargs):
        self.pin = pin
        self.in_open_state = False
        self.last_open = time.time()
        self.last_close = time.time()
        super(MagneticSwitch, self).__init__(**kwargs)

        # Set up the door sensor pin.
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

    def is_open(self):
        # 0 : Close // 1 : Open
        is_openning = bool(GPIO.input(self.pin))
        if is_openning and not self.in_open_state:
            self.in_open_state = True
            self.last_open = time.time()

        elif not is_openning and self.in_open_state:
            self.in_open_state = False
            self.last_close = time.time()
        return is_openning

    def is_recently_closed(self, duration_in_second=0.5):
        if time.time() - self.last_close < duration_in_second:
            return True
        else:
            return False

    def get_active_period(self):
        return self.last_close - self.last_open

    def cleanup(self):
        GPIO.cleanup()