"""SSD1306 demo (flip)."""
from time import sleep
from machine import Pin, I2C  # type: ignore
from xglcd_font import XglcdFont
from ssd1306 import Display


def test():
    """Test code."""
    i2c = I2C(1, freq=400000, scl=Pin(40), sda=Pin(41))  # Qt-Py S2 I2C bus 1
    display = Display(i2c=i2c, flip=False)  # Flip false

    print("Loading font.  Please wait.")
    bitstream = XglcdFont('fonts/Bitstream_Vera35x32.c', 35, 32)

    display.draw_bitmap("images/no_wifi32x32.mono", 0, 0, 32, 32, invert=True)
    display.draw_text(45, 0, "WiFi", bitstream)
    display.present()
    sleep(3)

    display.flip()  # Flip to 180 degrees which is the default
    display.present()
    sleep(3)

    display.flip(False)  # No flip (0 degrees)
    display.present()

    sleep(10)
    display.cleanup()
    print('Done.')


test()
