"""SSD1306 demo (fonts)."""
from time import sleep
from machine import Pin, I2C  # type: ignore
from xglcd_font import XglcdFont
from ssd1306 import Display


def test():
    """Test code."""
    i2c = I2C(1, freq=400000, scl=Pin(40), sda=Pin(41))  # Qt-Py S2 I2C bus 1
    display = Display(i2c=i2c)

    print("Loading fonts.  Please wait.")
    bally = XglcdFont('fonts/Bally7x9.c', 7, 9)
    rototron = XglcdFont('fonts/Robotron7x11.c', 7, 11)
    perfect = XglcdFont('fonts/PerfectPixel_23x32.c', 23, 32)
    wendy = XglcdFont('fonts/Wendy7x8.c', 7, 8)

    print("Drawing fonts.")

    display.draw_text(0, 0, "Perfect", perfect)
    x = bally.measure_text("Bally")
    display.draw_text(x, 23, "Bally", bally, rotate=180)
    display.fill_rectangle(105, 0, 9, 31)
    y = (display.height - wendy.measure_text("Wendy")) // 2
    display.draw_text(106, y, "Wendy", wendy, invert=True, rotate=90)
    display.draw_text(116, 32, "Roto", rototron, rotate=270)

    display.present()

    sleep(10)
    display.cleanup()
    print('Done.')


test()
