from lumos.lumos import Lumos, LumosPattern

import time

board = Lumos()

board.brightness(10)
#board.num_leds(20)

increment = True
while True:
    for x in range(1, 50):
        if increment:
            brightness = x
        else:
            brightness = 50 - x
        board.brightness(brightness)
        board.pattern(LumosPattern.BLUE)
        time.sleep(0.02)
    increment = not increment
    