"""SSD1306 demo (animation)."""
from framebuf import FrameBuffer, MONO_HMSB  # type: ignore
import gc
from machine import Pin, I2C  # type: ignore
from micropython import const  # type: ignore
from ssd1306 import Display
from utime import sleep_us, ticks_us, ticks_diff  # type: ignore

SPRITE_WIDTH = const(12)
SPRITE_HEIGHT = const(13)
SPRITE_COUNT = const(4)
SIZE = const(26)  # 2 bytes wide x 13 tall (1 bit per pixel)


def draw_dots(dots, start_x, y, display):
    """Draw dots for Pac-Man to eat.

    Args:
        dots(int): The number of dots to draw
        start_x(int): The x position of the first dot
        y(int): The y position of the dots
        display(DISPLAY): Display to draw to
    """
    step = (display.width - start_x) // dots
    end_x = start_x + (step * dots)
    for x in range(start_x, end_x, step):
        display.fill_circle(x, y, 2)


def test():
    """Test code."""
    i2c = I2C(1, freq=400000, scl=Pin(40), sda=Pin(41))  # Qt-Py S2 I2C bus 1
    display = Display(i2c=i2c)
    display.clear()

    # Load sprite sheet
    pacman = display.load_sprite('images/pacman_sprite12x52.mono',
                                 SPRITE_WIDTH, SPRITE_HEIGHT * SPRITE_COUNT,
                                 invert=True)

    # Create frame to hold sprites
    frames = [
        FrameBuffer(bytearray(SIZE), SPRITE_WIDTH, SPRITE_HEIGHT, MONO_HMSB),
        FrameBuffer(bytearray(SIZE), SPRITE_WIDTH, SPRITE_HEIGHT, MONO_HMSB),
        FrameBuffer(bytearray(SIZE), SPRITE_WIDTH, SPRITE_HEIGHT, MONO_HMSB),
        FrameBuffer(bytearray(SIZE), SPRITE_WIDTH, SPRITE_HEIGHT, MONO_HMSB)
    ]

    for i in range(SPRITE_COUNT):
        # Copy the frames from the sprite sheet
        for y in range(SPRITE_HEIGHT):
            for x in range(SPRITE_WIDTH):
                frames[i].pixel(x, y, pacman.pixel(x, y + (SPRITE_HEIGHT * i)))

    x = 2
    y = (display.height - SPRITE_HEIGHT) // 2
    x_min = 2
    x_max = (display.width - 1) - (SPRITE_WIDTH + 2)
    index = 0  # Sprite frame index
    x_speed = 2  # Horizontal speed
    draw_dots(7, 26, y + (SPRITE_HEIGHT // 2), display)

    try:
        while True:
            timer = ticks_us()
            offset = int(-3.5 * x_speed + 5)  # Offset to clear previous image
            display.fill_rectangle(x + offset, y, 2, SPRITE_HEIGHT,
                                   invert=True)  # Clear previous image
            f = -(x_speed // 2) + 1 + index  # Get current frame
            display.draw_sprite(frames[f], x, y,  # Draw Pac-Man
                                SPRITE_WIDTH, SPRITE_HEIGHT)
            display.present()
            index = (index + 1) % 2  # Next sprite index (wrap on last)
            # Attempt to set framerate to 5 FPS
            timer_dif = 200000 - ticks_diff(ticks_us(), timer)
            if timer_dif > 0:
                sleep_us(timer_dif)
            x += x_speed  # Increment x position
            if x >= x_max:  # Change direction at max
                x = x_max
                x_speed = -abs(x_speed)
                gc.collect()
            if x <= x_min:  # Change direction at min
                x = x_min
                x_speed = abs(x_speed)
                draw_dots(8, 26, y + (SPRITE_HEIGHT // 2), display)
                gc.collect()
    except KeyboardInterrupt:
        display.cleanup()
    finally:
        display.cleanup()
        print('Done.')


test()
