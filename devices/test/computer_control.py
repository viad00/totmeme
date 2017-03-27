from machine import Pin
import time

def power_on(dev_pin, timer=1):
    Pin(dev_pin, Pin.OUT).high()
    time.sleep(timer)
    Pin(dev_pin, Pin.OUT).low()

def force_stop(dev_pin, timer=10):
    Pin(dev_pin, Pin.OUT).high()
    time.sleep(timer)
    Pin(dev_pin, Pin.OUT).low()
