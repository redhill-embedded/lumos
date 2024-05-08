import argparse

import lumos
from lumos.lumos import Lumos, LumosPowerState, LumosMode, LumosPattern
from recom import RecomDevice, RecomDeviceException


def print_info():
    board = Lumos()
    print(f"Number of LEDs = {board.interface.get_num_leds()}")
    print(f"Power state = {board.interface.get_power_state()}")
    print(f"Voltage = {board.interface.get_voltage_reading()}mV")
    print(f"Current = {board.interface.get_current_reading()}mA")
    print(f"Brightness = {board.interface.get_brightness()}")

def power_ctrl(arg):
    board = Lumos()
    if "on" in arg or "ON" in arg or "On" in arg:
        print("Turning power ON")
        board.interface.set_power_state(LumosPowerState.POWER_ON)
    else:
        print("Turning power OFF")
        board.interface.set_power_state(LumosPowerState.POWER_OFF)

def set_pattern(arg):
    board = Lumos()
    board.interface.set_power_state(LumosPowerState.POWER_ON)
    board.interface.set_mode(LumosMode.MANUAL)
    pattern = arg[0].upper()
    for p in LumosPattern:
        if pattern in p.name:
            print(f"Setting pattern {p}")
            board.interface.set_pattern(p.value)


def set_brightness(arg):
    brightness = int(arg[0])
    if brightness > 100:
        print(f"ERROR: Brightness should be a number between 0 and 100. You typed {brightness}")
        return
    print(f"Setting brightness to {brightness}")
    board = Lumos()
    board.interface.set_brightness(brightness)


def cli(argv):
    parser = argparse.ArgumentParser(description="Lumos CLI to interract with an LED controller board.")
    parser.add_argument("cmd", type=str, help="Command/Action")
    parser.add_argument('--version', action='version', version=lumos.__version__,
                                                help="Print package version")
    parser.add_argument('-S', '--serial', help='Serial number to search for')

    args, remaining_args = parser.parse_known_args(argv)

    if args.cmd == "info":
        print_info()
    elif args.cmd == "power":
        power_ctrl(remaining_args)
    elif args.cmd == "pattern":
        set_pattern(remaining_args)
    elif args.cmd == "brightness":
        set_brightness(remaining_args)
