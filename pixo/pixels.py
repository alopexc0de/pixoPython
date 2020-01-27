import time
import random
from board import TOTAL_DOTS, BOARD

class Pixo:
    """
        Class that provides ease of life methods for
        displaying content on the board.

        During boot, `BOARD.auto_write` is set to False,
        which prevents newly written data from immediately
        updating the content. Call `BOARD.show()` whenever
        you want content to be updated.
    """

    def _random_color(self):
        """
            Generates a random value from 0-224
        """
        return random.randrange(0, 7) * 32

    def clear(self):
        """
            Fills the board with a 0 value and updates
            the content, turning off all LEDs
        """
        self.fill((0, 0, 0))
        BOARD.show()

        return self

    def fill(self, color):
        """
            Fills the board with an RGB value, provided
            via `color` as either a list or tuple
        """
        BOARD.fill(color)
        BOARD.show()

        return self

    def fill_image(self, image, show=True, slow=False):
        """
            Fills the board with the provided `image`,
            which is a list of tuples containing RGB values

            When `show` is False, the board will not be updated
            automatically. This is useful if chaining commands
            together (such as setting the image, and then forcing
            a specific color for active pixels in the image)

            When `slow` is True, the content is updated pixel
            by pixel, rather than all at once
        """
        for dot in range(TOTAL_DOTS):
            BOARD[dot] = image[dot]
            if slow and show:
                BOARD.show()
        if not slow and show:
            BOARD.show()

        return self

    def fill_random(self, slow=False):
        """
            Fills the board with random RGB values

            When `Slow` is True, the content is updated pixel
            by pixel, rather than all at once
        """
        for dot in range(TOTAL_DOTS):
            BOARD[dot] = (
                self._random_color(),
                self._random_color(),
                self._random_color()
            )
            if slow:
                BOARD.show()
        if not slow:
            BOARD.show()

        return self

    def blink_image(self, image, force=(), delay=0.3):
        """
            Fills the board with the provided `image`,
            which is a list of tuples containing RGB values

            When `force` is set, it should be a tuple of
            RGB values; it will override all colors on the
            board that are active.

            `delay` is a float of how many seconds to wait
            before the board gets blanked out.

            To blink multiple times, call this in a loop
        """
        if len(force) == 0:
            self.fill_image(image)
        else:
            self.fill_image(image, False).force_color(force)
        time.sleep(delay)
        self.fill((0, 0, 0))

        return self

    def force_color(self, color):
        for dot in range(TOTAL_DOTS):
            if BOARD[dot] != (0, 0, 0) and BOARD[dot] != color:
                BOARD[dot] = color
        BOARD.show()

        return self

    def transition_image_random(self, image, delay=0.2):
        """
            Changes a random pixel to the value of that
            pixel on a newly provided `image`.

            `delay` is how many seconds to wait between
            changing each pixel

            Prevents the same random value from being
            selected multiple times
        """
        already_changed = []
        while len(already_changed) < TOTAL_DOTS:
            dot = random.randrange(0, TOTAL_DOTS)
            if dot not in already_changed and not BOARD[dot] == image[dot]:
                already_changed.append(dot)

                BOARD[dot] = image[dot]
                time.sleep(delay)
                BOARD.show()
            
        return self

    def transition_image_dissolve(self, delay=0.2):
        """
            Randomly sets pixels to black, giving the
            appearance of it dissolving away into the ether

            `delay` is how many seconds to wait between
            changing each pixel
        """
        return self.transition_image_random((0, 0, 0), delay)

    # This doesn't give the desired cycle that a gaming keyboard would
    # def color_cycle(self):
    #     for r in range(100, 200):
    #         for g in range(100, 200):
    #             for b in range(100, 200):
    #                 print((r, g, b))
    #                 self.fill((r, g, b))
