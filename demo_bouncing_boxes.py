"""SSD1306 demo (bouncing boxes)."""
from machine import Pin, I2C  # type: ignore
from random import random, seed
from ssd1306 import Display
from utime import sleep_us, ticks_cpu, ticks_us, ticks_diff  # type: ignore


class Box(object):
    """Bouncing box."""

    def __init__(self, screen_width, screen_height, size, display):
        """Initialize box.
        Args:
            screen_width (int): Width of screen.
            screen_height (int): Width of height.
            size (int): Square side length.
            display (SSD1306): OLED display object.
        """
        self.size = size
        self.w = screen_width
        self.h = screen_height
        self.display = display

        # Generate non-zero random speeds between -5.0 and 5.0
        seed(ticks_cpu())
        r = random() * 10.0
        self.x_speed = 5.0 - r if r < 5.0 else r - 10.0
        r = random() * 10.0
        self.y_speed = 5.0 - r if r < 5.0 else r - 10.0

        self.x = self.w / 2.0
        self.y = self.h / 2.0
        self.prev_x = self.x
        self.prev_y = self.y

    def update_pos(self):
        """Update box position and speed."""
        x = self.x
        y = self.y
        size = self.size
        w = self.w
        h = self.h
        x_speed = self.x_speed
        y_speed = self.y_speed
        self.prev_x = x
        self.prev_y = y

        # Update x position and handle boundaries
        x += x_speed
        if x + size >= w - 1:
            x = (w - 1) - (size + 1)
            self.x_speed = -abs(x_speed)
        elif x < 1:
            x = 1
            self.x_speed = abs(x_speed)
        self.x = x

        # Update y position and handle boundaries
        y += y_speed
        if y + size > h - 1:
            y = (h - 1) - (size + 1)
            self.y_speed = -abs(y_speed)
        elif y < 1:
            y = 1
            self.y_speed = abs(y_speed)
        self.y = y

    def draw(self):
        """Draw box."""
        x = int(self.x)
        y = int(self.y)
        size = self.size
        prev_x = int(self.prev_x)
        prev_y = int(self.prev_y)
        self.display.fill_rectangle(prev_x,
                                    prev_y,
                                    size, size, invert=True)
        self.display.fill_rectangle(x,
                                    y,
                                    size, size)
        self.display.present()


def test():
    """Bouncing box."""
    try:
        i2c = I2C(1, freq=400000, scl=Pin(40), sda=Pin(41))
        display = Display(i2c=i2c)
        display.clear()

        sizes = [8, 7, 6, 5, 4, 3]
        boxes = [Box(128, 32, sizes[i], display) for i in range(len(sizes))]

        display.fill_rectangle(0, 0, 128, 32)

        while True:
            timer = ticks_us()
            for b in boxes:
                b.update_pos()
                b.draw()
            # Attempt to set framerate to 30 FPS
            timer_dif = 33333 - ticks_diff(ticks_us(), timer)
            if timer_dif > 0:
                sleep_us(timer_dif)

    except KeyboardInterrupt:
        display.cleanup()


test()
