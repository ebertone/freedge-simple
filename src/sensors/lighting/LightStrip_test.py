"""Test for Lightstrip"""
from neopixel import *
from LightStrip import LightStrip

if __name__ == '__main__':
  # Create NeoPixel object with appropriate configuration.
  strip = LightStrip()
  try:
    while True:
      print ('Color wipe animations.')
      strip.colorWipe(Color(255, 0, 0))  # Red wipe
      strip.colorWipe(Color(0, 255, 0))  # Blue wipe
      strip.colorWipe( Color(0, 0, 255))  # Green wipe
      print ('Theater chase animations.')
      strip.theaterChase(Color(127, 127, 127))  # White theater chase
      strip.theaterChase(Color(127,   0,   0))  # Red theater chase
      strip.theaterChase(Color(  0,   0, 127))  # Blue theater chase
      print ('Rainbow animations.')
      strip.rainbow()
      strip.rainbowCycle()
      strip.theaterChaseRainbow()
  except KeyboardInterrupt:
      strip.colorWipe(Color(0,0,0), 10)
