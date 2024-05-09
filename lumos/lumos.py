
from enum import IntEnum
import struct

from recom import RecomDevice


class LumosOpcode(IntEnum):
    NUM_LEDS    = 0
    MODE        = 1
    POWER_STATE = 2
    VOLTAGE     = 3
    CURRENT     = 4
    BRIGHTNESS  = 5
    PATTERN     = 6
    SET_ALL     = 7
    SET_ONE     = 8
    CLEAR_ALL   = 9


class LumosPowerState(IntEnum):
    POWER_OFF   = 0
    POWER_ON    = 1

class LumosMode(IntEnum):
    IDLE = 0,
    STREAMING = 1,
    MANUAL = 2

class LumosPattern(IntEnum):
    RED     = 0,
    GREEN   = 1,
    BLUE    = 2,
    WHITE   = 3,


class LumosInterface():

    KNOWN_VID_PID = ["2e8a:a701"]
    ITF_ID = 0x30
    ITF_PROT = 0x00

    def __init__(self):
        self.device = RecomDevice(id=self.KNOWN_VID_PID[0])
        if self.device is None:
            raise Exception("No Lumos device found!")
        self.interface = self.device.getInterfaceHandleFromID((self.ITF_ID, self.ITF_PROT))
        if self.interface is None:
            raise Exception("No Lumos interface found!")

    def get_num_leds(self) -> int:
        data = self.interface.controlRead(request=LumosOpcode.NUM_LEDS)
        num_leds, = struct.unpack("<H", data)
        return num_leds

    def set_num_leds(self, num_leds: int):
        data = struct.pack("<H", num_leds)
        self.interface.controlWrite(request=LumosOpcode.NUM_LEDS, data=data)

    def get_mode(self) -> int:
        data = self.interface.controlRead(request=LumosOpcode.MODE)
        mode, = struct.unpack("<B", data)
        return mode

    def set_mode(self, mode: LumosMode):
        data = struct.pack("<B", mode)
        self.interface.controlWrite(request=LumosOpcode.MODE, data=data)

    def get_power_state(self) -> LumosPowerState:
        data = self.interface.controlRead(request=LumosOpcode.POWER_STATE)
        power_state, = struct.unpack("<B", data)
        return power_state

    def set_power_state(self, power_state: LumosPowerState):
        data = struct.pack("<B", power_state)
        self.interface.controlWrite(request=LumosOpcode.POWER_STATE, data=data)

    def get_voltage_reading(self) -> int:
        data = self.interface.controlRead(request=LumosOpcode.VOLTAGE)
        voltage_mv, = struct.unpack("<H", data)
        return voltage_mv

    def get_current_reading(self) -> int:
        data = self.interface.controlRead(request=LumosOpcode.CURRENT)
        current_ma, = struct.unpack("<H", data)
        return current_ma

    def get_brightness(self) -> int:
        data = self.interface.controlRead(request=LumosOpcode.BRIGHTNESS)
        brightness, = struct.unpack("<B", data)
        return brightness

    def set_brightness(self, brightness: int):
        data = struct.pack("<B", brightness)
        self.interface.controlWrite(request=LumosOpcode.BRIGHTNESS, data=data)

    def set_pattern(self, pattern: LumosPattern):
        data = struct.pack("<B", pattern)
        self.interface.controlWrite(request=LumosOpcode.PATTERN, data=data)

    def set_all(self, red: int, green: int, blue: int):
        data = struct.pack("<BBB", red, green, blue)
        self.interface.controlWrite(request=LumosOpcode.SET_ALL, data=data)

    def set_one(self, index: int, red: int, green: int, blue: int):
        data = struct.pack("<BBBB", index, red, green, blue)
        self.interface.controlWrite(request=LumosOpcode.SET_ONE, data=data)

    def clear_all(self):
        self.interface.controlWrite(request=LumosOpcode.CLEAR_ALL)

    def send_led_stream(self, data: bytearray):
        self.interface.write(data)

class Lumos():

    def __init__(self, **kwargs):
        self.interface = LumosInterface()

    def brightness(self, brightness):
        self.interface.set_brightness(brightness)

    def pattern(self, pattern):
        self.interface.set_pattern(pattern)

    def num_leds(self, num_leds):
        self.interface.set_num_leds(num_leds)

    def color(self, red: int, green: int, blue: int):
        self.set_all(red, green, blue)

    def set_all(self, red: int, green: int, blue: int):
        self.interface.set_all(red, green, blue)

    def set_one(self, index: int, red: int, green: int, blue: int):
        self.interface.set_one(index, red, green, blue)

    def clear(self):
        self.interface.clear_all()
