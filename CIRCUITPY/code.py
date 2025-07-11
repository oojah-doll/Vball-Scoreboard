import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D13, 70, brightness = 0.5)

while True:
    print('lights on')
    pixels.fill((0, 255, 0))
    time.sleep(5)
    print('whatever2')
    pixels.fill((0, 0, 0))
    time.sleep(5)