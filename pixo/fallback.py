# Setup network
import network
import time

# Hardcoded network credentials
try:
    import creds
except ImportError:
    class creds:
        WIFI_NETWORKS = [
            ('', '')
        ]

# We will attempt connections for this many seconds
MAX_WAIT = 15

# Setup the wifi connection
STA_IF = network.WLAN(network.STA_IF)

if not STA_IF.isconnected():
    for network in creds.WIFI_NETWORKS:
        if STA_IF.isconnected():
            break
        STA_IF.connect(network[0], network[1])

import uftpd
