# This file is executed on every boot (including wake-boot from deepsleep)
# Be careful about doing things that loop here, you may have to reinstall the firmware

# import esp
# esp.osdebug(None)

# Initalize the board
from board import TOTAL_DOTS, BOARD

# Class that contains display methods, animations, etc
from pixels import Pixo
# Blank the display
Pixo().clear()

# Small ease of use methods
from helpers import *

# Setup wifi connection
import wifi

# Start an anonymous FTP server (TODO: Do this on the AP_IF only)
import uftpd
