# PixoPython Server

This is a small python server that uses [Bottle](https://bottlepy.org) to provide an encrypted REST interface to the pixo firmware (and future compatibles).

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
  - Does not allow changing of `/data/config` commands
  - Does not allow `/sensor` commands, the bot will poll for sensor endpoints automatically. These sensors can be later removed by
    1. `/device edit name`
    2. `/sensor del sensor-name`
- `/deldevice [name/id]` - Alias of `/device del [name/id]`
- `/ping [name/id]` - Alias of `/device [name/id] ping`

- `/device [new/edit/del] [name/id] [opts]` - `[opts]` are sub-commands to run directly. **Enters Device Configuration Mode** with the following commands. 
  - /exit - Returns to normal mode

  - /connect - Connects to the device with various options
    1. /device (default) - The device will connect to the server from time to time (configurable in device settings). Generates a shared secret to be inputted in device settings
    2. /discover - If the device is on the same network as the server, we can attempt autodiscovery and the server will establish a connection
      - The device should prompt for acceptance, either via button press or other UI
    3. /direct - If the device can be accessed with a hostname/domain/IP:port, the server will establish a connection
      - The device should prompt for acceptance, either via button press of other UI

  - /data - Provides meta-data about the device
    1. /resolution - Dimensions of device. Expects to be in format like 16x16
    2. /name - Sets a unique to you name for the device, any length
    3. /type - What type of device is it (eg. pixo-pixel)
  - /auto [on/off] - If on, the device will automatically recieve any media sent to the bot, if the media is supported. Default off

  - /protect - User will be prompted to input a pin that will not be displayed. Prevents further changes to the **device configuration**
    1. This does not prevent reading of known sensors, use `/sensor del [name]` to remove and make inaccessable
    2. When sent again, the user will be asked if they want to remove the protection
  
  - /sensor [add/del] [name] [endpoint] - If a sensor is not automatically detected, or you wish to remove a sensor, this will communicate to the device and 
  - /read [sensor] - If the device has the named sensor, read the value and return it
    1. The sensor can be physical (ie, temperature, gyroscope, etc) or it can be virtual (ie, CPU/MEM utilization, WIFI traffic, etc)
  - /poll [sensor] [timer] - Performs a `/read` every `timer` seconds
    1. Every new message will include a button to stop the timer/stop button will be available in custom keyboard as priority option
  
  - /ping - Pings the selected device and responds with how long it took/offline. 
  - /cmd [cmd] [opts] - Sends an API request to the selected device with the selected command with options
    1. These API requests are *in the documetation for the device*
  - /config [option] [value] - If supported, sets/replaces device config option (ex, change wifi, secret key, etc)
    1. If the device has been `/protect`ed, these changes will fail

### Images

When the bot recieves an image, we need to resize it to our matrix resolution

### Animations

### Video (maybe)

# LICENSE

MIT, Refer to the `license` file in the project root
