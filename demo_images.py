"""SSD1306 demo (images)."""
from time import sleep
from machine import Pin, I2C  # type: ignore
from ssd1306 import Display


def test():
    """Test code."""
    # spi = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(13))
    # display = Display(spi, dc=Pin(4), cs=Pin(5), rst=Pin(2))
    i2c = I2C(1, freq=400000, scl=Pin(40), sda=Pin(41))  # Qt-Py S2 I2C bus 1
    display = Display(i2c=i2c)

    display.draw_bitmap("images/inazuma128x32.mono", 0, 0, 128, 32)
    display.present()
    sleep(5)

    display.clear_buffers()
    x = (display.width - 48) // 2
    y = (display.height - 26) // 2
    display.draw_bitmap("images/saucer_48x26.mono", x, y, 48, 26,
                        invert=True)

    for coords in ((0, 0), (6, 22), (20, 14), (32, 0), (95, 0), (105, 14),
                   (119, 22), (119, 0)):
        display.draw_bitmap("images/invader8x8.mono", *coords, 8, 8,
                            invert=True)
    display.present()
    sleep(5)

    display.clear_buffers()
    display.fill_rectangle(0, 0, 128, 32)
    display.draw_bitmap("images/wwhite22x29.mono", 1, 1, 22, 29)
    display.draw_bitmap("images/wwhite22x29.mono", 28, 5, 22, 29, rotate=90)
    display.draw_bitmap("images/wwhite22x29.mono", 66, 5, 22, 29, rotate=270)
    display.draw_bitmap("images/wwhite22x29.mono", 100, 1, 22, 29, rotate=180)

    display.present()

    sleep(10)
    display.cleanup()
    print('Done.')


test()
