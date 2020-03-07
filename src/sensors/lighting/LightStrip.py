#!/usr/bin/env python
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class LightStrip():

  def __init__(self):
    # Create NeoPixel object with appropriate configuration.
    self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    self.strip.begin()

  def turn_off(self):
    self.colorWipe(Color(0,0,0), 3)

  def flash(self):
    """Animate Flashing Effect"""
    self.colorWipe(Color(127, 127, 127), 3)
    time.sleep(0.3)
    self.colorWipe(Color(127, 127, 127), 3)
    time.sleep(0.5)
    self.colorWipe(Color(127, 127, 127), 3)


  # Define functions which animate LEDs in various ways.
  def colorWipe(self, color, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, color)
      self.strip.show()
      time.sleep(wait_ms/1000.0)

  def theaterChase(self, color=Color(127, 127, 127), wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
      for q in range(3):
        for i in range(0, self.strip.numPixels(), 3):
          self.strip.setPixelColor(i+q, color)
        self.strip.show()
        time.sleep(wait_ms/1000.0)
        for i in range(0, self.strip.numPixels(), 3):
            self.strip.setPixelColor(i+q, 0)

  def wheel(self, pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
      return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
      pos -= 85
      return Color(255 - pos * 3, 0, pos * 3)
    else:
      pos -= 170
      return Color(0, pos * 3, 255 - pos * 3)

  def rainbow(self, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
      for i in range(self.strip.numPixels()):
        self.strip.setPixelColor(i, self.wheel((i+j) & 255))
      self.strip.show()
      time.sleep(wait_ms/1000.0)

  def rainbowCycle(self, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
      for i in range(self.strip.numPixels()):
        self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
      self.strip.show()
      time.sleep(wait_ms/1000.0)

  def theaterChaseRainbow(self, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
      for q in range(3):
        for i in range(0, self.strip.numPixels(), 3):
          self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
        self.strip.show()
        time.sleep(wait_ms/1000.0)
        for i in range(0, self.strip.numPixels(), 3):
          self.strip.setPixelColor(i+q, 0)
