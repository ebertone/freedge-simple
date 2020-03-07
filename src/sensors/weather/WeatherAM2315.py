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
from ..Sensor import Sensor
from tentacle_pi.AM2315 import AM2315

class WeatherAM2315(Sensor):
  """"AM2315 sensor measures temperature and humidity 
  in the environment.
  """
  def __init__(self, address, i2c_port="/dev/i2c-1", **kwargs):
    super(WeatherAM2315, self).__init__(**kwargs)
    self.am2315 = AM2315(address, i2c_port)

  def sense(self, max_attempts=3):
    num_attempts = 0
    while True:
      temp, humid, ok = self.am2315.sense()
      if ok == 1:
        break
      else:
        num_attempts += 1
        print("Weather sensor is temporarily unavailable. Attempting to connect ({}/{})".format(
              num_attempts,max_attempts))
        time.sleep(0.5)
        if num_attempts >= max_attempts:
          print("Please check weather sensor connection.")
          break
    return temp, humid, ok