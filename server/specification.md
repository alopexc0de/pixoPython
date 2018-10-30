# PixoPython Server API

This is the specification for the PixoPython Server. 

- API - These are external functions and/or HTTP routes of the server
- pixo - This is the HTTP REST API specified by the `pixo firmware`
- Telegram Bot - This is a thread of the API server that connects to Telegram as a Bot to recieve media

## API->pixo Definition

TBD

## Web->API Definition

TBD

## Telegram Bot->API Definition

Initial implementation will use [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) to create a Telegram interface that accepts 
- Commands
- Images
- Animations
- Videos (This one is low priority/might not happen)

### Commands

For all commands that accept, but aren't supplied a specific input, the bot will automatically provide context-aware options (such as names of enrolled devices) or inputs (custom keyboard/number keyboard/normal keyboard)

- `/send [name/id] *ATTACHMENT*` - Sends the attached media (if supported) to the selected device. 
  - If `/auto` is configured for any device, simply forwarding media to the bot will `/send` it to the device(s)
- `/newdevice [name/id]` - Alias of `/device new [name/id]`, if no name provided, starts "New Device Wizard", a series of `/device` sub-commands to get started
  - Runs through these sub-commands
    1. `/connect`
    2. `/data` - Name, resolution, and type
    3. `/auto` - Read `/send` above
    4. `/protect` - Prevent further changes to the device until turned off, unique per device pin
  - Does not allow changing of `/config` commands
  - Does not allow `/sensor` commands, the bot will poll for sensor endpoints automatically. These sensors can be later removed by
    1. `/device edit name`
    2. `/sensor del sensor-name`
- `/deldevice [name/id]` - Alias of `/device del [name/id]`
  - If the device has `/protect` turned on, the user must enter the pin before confirming the deletion
- `/ping [name/id]` - Pings the selected device and responds with how long it took/offline. 

- `/device [new/edit/del] [name/id]` - New enrolls a new device, Del will purge the device from the database, Edit engages **Device Configuration Mode** with the following available commands. 
  - `/exit` - Returns to normal mode
    1. If `/protect` is not on, the user will be asked if they want to enable it 

  - `/connect` - Connects to the device with various options
    1. `/device` (default) - The device will connect to the server from time to time (configurable in device settings). Generates a shared secret to be inputted in device settings
    2. `/discover` - If the device is on the same network as the server, we can attempt autodiscovery and the server will establish a connection
      - The device should prompt for acceptance, either via button press or other UI
    3. `/direct` - If the device can be accessed with a hostname/domain/IP:port, the server will establish a connection
      - The device should prompt for acceptance, either via button press of other UI

  - `/data` - Provides meta-data about the device
    1. `/resolution` - Dimensions of device. Expects to be in format like 16x16
    2. `/name` - Sets a unique to you name for the device, any length
    3. `/type` - What type of device is it (eg. pixo-pixel)
  - `/auto [on/off]` - If on, the device will automatically recieve any media sent to the bot, if the media is supported. Default off

  - `/protect [on/off/clear]` - User will be prompted to input a pin that will not be displayed. Prevents further changes to **all device configuration**
    1. This does not prevent reading of known sensors, use `/sensor del [name]` to remove and make them inaccessable when `/protect` is off
      - This prevents deletion and addition of sensors if enabled
    2. When sent again, the user will be asked if they want to remove the protection
    3. If the user attempts to delete the device, and `/protect` is on, they will first be prompted for their device pin
    4. If the user attempts to edit the device, they will be told to turn off `/protect` first
    5. If off, `/protect` will remember the last set pin. Use `/protect clear` to remove the pin
  
  - `/sensor [add/del] [name] [endpoint]` - If a sensor is not automatically detected, or you wish to remove a sensor, this will communicate to the device and read the value. 
    1. If the device does not have the endpoint, the sensor will not be added
  - `/read [sensor]` - If the device has the named sensor, read the value and return it
    1. The sensor can be physical (ie, temperature, gyroscope, etc) or it can be virtual (ie, CPU/MEM utilization, WIFI traffic, etc)
  - `/poll [sensor] [timer]` - Performs a `/read` every `timer` seconds
    1. Every new message will include a button to stop the timer/stop button will be available in custom keyboard as priority option
  
  - `/cmd [cmd] [opts]` - Sends an API request to the selected device with the selected command with options
    1. These API requests are *in the documetation for the device*
  - `/config [option] [value]` - If supported, sets/replaces device config option (ex, change wifi, secret key, etc)
    1. If the device has been `/protect`ed, these changes will fail

### Images

When the bot recieves an image, we need to do the following

1. Check for any bots that have the `auto` flag enabled, and for those bots
  - Apply any filters
  - resize the image to the device resolution
  - Apply transition to/from this image if applicable
  - Queue the message to be sent to the device, if verbose mode send message when device recieves it
2. Ask user which device they want to send the image to and follow `auto` steps

### Animations

Depending on the frame rate, this could be just a bunch of images that get sent through. 
Perhaps a compression scheme may be needed. May require a bit of processing on the device.

### Video (maybe)

Even faster than animations, and generally require a bit of processing on the device
