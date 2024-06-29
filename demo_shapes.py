"""SSD1306 demo (shapes)."""
from time import sleep
from machine import Pin, I2C  # type: ignore
from ssd1306 import Display


def test():
    """Test code."""
    i2c = I2C(1, freq=400000, scl=Pin(40), sda=Pin(41))  # Qt-Py S2 I2C bus 1
    display = Display(i2c=i2c)

    display.draw_rectangle(6, 6, 16, 16)
    display.fill_rectangle(9, 9, 10, 10)

    display.draw_line(24, 31, 32, 0)

    display.fill_circle(48, 16, 14)
    display.draw_circle(48, 16, 10, invert=True)

    coords = [(117, 0), (117, 31), (96, 6), (127, 16), (96, 26), (117, 0)]
    display.draw_lines(coords)

    display.draw_pixel(0, 0)
    display.draw_pixel(127, 0)
    display.draw_pixel(0, 31)
    display.draw_pixel(127, 31)

    display.fill_ellipse(81, 16, 15, 8)
    display.draw_ellipse(81, 16, 8, 15)

    display.fill_polygon(3, 48, 16, 6, invert=True)
    display.draw_polygon(6, 81, 16, 6, invert=True)

    display.present()

    sleep(6)
    display.cleanup()
    print('Done.')


test()
