import os
from machine import Timer
from board import TOTAL_DOTS

def cat(filename, content=False):
    """
        Simulation of an OS's `cat`

        `filename` is either a full or relative path
        to a file to interact with.

        When `content` is not provided, the contents
        of the file will be printed out. When provided,
        `content` is expected to be a string-like value
        that will be written to `filename`
    """
    mode = 'r'
    if content:
        mode = 'w'
    with open(filename, mode) as file:
        if content:
            file.write(content)
        else:
            print(''.join(file.readlines()))
    file.close()

def ls(path=''):
    """
        Prints out the contents of a directory.

        When `path` is defined, it's expected to
        be string containing the full or relative
        path to a destination
    """
    print('ls %s' % path)
    print('\n'.join(os.listdir()))

class TimeLoop:
    """
        If you have an iterable (such as the BOARD),
        you can use this class to run some code
        asyncronously; which will still allow interactive
        commands on the REPL.

        Available methods:

        `self.st(callback)` - Starts the timer running
        and will run `callback` every self.timer_speed ms

        `self.s()` - Completely stops the timer

        Arguments at initialization:

        `timer_speed` is required, and will determine
        how often (in ms) `self.st(callback)` will be
        triggered. (You can't call `callback` from `self`)

        `timer_id` is optional, and should only be used
        when you want to run multiple timers concurrently
    """
    def __init__(self, timer_speed, timer_id=-1):
        self.timer = Timer(timer_id)
        self.timer_speed = timer_speed

    def st(self, callback):
        self.timer.init(
            period=self.timer_speed,
            mode=Timer.PERIODIC,
            callback=lambda self: callback()
        )

    def s(self):
        self.timer.deinit()
