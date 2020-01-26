import micropython_dotstar as dotstar
from machine import Pin, SPI

# Configure some globals, such as the LED board
TOTAL_DOTS = 256
DOTSTAR_CLOCK = Pin(18)
DOTSTAR_TX = Pin(19)
DOTSTAR_RX = Pin(17) # Note: This is unused as the LEDs don't send data back

# Setup the LED board
DOTSTAR_SPI = SPI(sck=DOTSTAR_CLOCK, mosi=DOTSTAR_TX, miso=DOTSTAR_RX)
BOARD = dotstar.DotStar(DOTSTAR_SPI, TOTAL_DOTS, brightness=0.2, auto_write=False)