# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola and Dylan McGlothin
# License: Public Domain
import json
import time
import datetime
import sqlite3
import os

# Import SPI library(for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO

# Software SPI configuration: 
# CLK = 18
# MISO = 23
# MOSI = 24
# CS = 25
# mcp = Adafruit_MCP3008.MCP3008(clk = CLK, cs = CS, miso = MISO, mosi = MOSI)

# Hardware SPI configuration:
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi = SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# GPIO Config
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)

# Relay Config
def relayOn():
  GPIO.output(17, GPIO.HIGH)
def relayOff():
  GPIO.output(17, GPIO.LOW)

print('Reading MCP3008 values, press Ctrl-C to quit...')# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format( * range(8)))
print('-' * 57)

# Main program loop.
while True:
  conn = sqlite3.connect('brotanicals.db')
  c = conn.cursor()# Read all the ADC channel values in a list.
  values = [0] * 8
  for i in range(8): 
# The read_adc function will get the value of the specified channel(0 - 7).
    values[i] = mcp.read_adc(i)
    percValue = ((mcp.read_adc(0) + mcp.read_adc(1)) / 2) / 10

# Make JSON data
    sensorData = {'name':'moisture1', 'val':percValue}
    with open('sensors.json', 'w') as outfile:
        json.dump(sensorData, outfile)
# Turn on relay
    if mcp.read_adc(0) < 25:
      relayOn()
    else :
      relayOff()
    stream.write({
    'x': datetime.datetime.now(),
    'y': percValue
    })

# Print the ADC values.
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format( * values))

# Pause for a second.
    time.sleep(1)
    
# Upload data to website
os.system("scp brotanicals.db uni@138.197.120.43:~/brotanicals/sensors.json")