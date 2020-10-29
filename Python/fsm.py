from enum import Enum, auto
import random
import struct
import sys
from modem import Modem
import modemdefs as ModemDefs
import time


class State(Enum):
    INIT = auto()
    JOINING = auto()
    READY = auto()
    TRANSMITTING = auto()


class Application:
    def __init__(self,
                 ser_port='/dev/ttyUSB0',
                 port=1,
                 period=300):
        """
        Simple application transmitting every period seconds.
        The application is intended to simulate an MCU application, it
        therefore assumes that the modem is reset before executing run()
        """
        self.m = Modem(ser_port)
        self.state = State.INIT
        self._poll_time = 1
        self._period = period
        self._clock = period
        self._port = port
    
    def measure(self):
        # Simulates a temperature sensor (for instance)
        value = round(random.uniform(17.0, 24.0),1)
        print(f"Sensor measure: {value} C")
        return  bytearray(struct.pack("f", value))

    def _get_event(self):
        try:
            evt = self.m.getevent()
            return evt
        except Exception as ex:
            print(f"Exception: {ex}")
            return None

    def _get_state(self):
        time.sleep(self._poll_time)
        evt = self._get_event()
        if evt is not None:
            if evt.type == ModemDefs.EVT_RESET:
                self.state = State.INIT
            elif evt.type == ModemDefs.EVT_JOINED:
                print("EVT JOINED")
                self.state = State.READY
            elif evt.type == ModemDefs.EVT_TXDONE:
                if evt.data == b'\x00':
                    print("EVT TXDONE. Package NOT sent!")
                elif evt.data == b'\x01':
                    print("EVT TXDONE. Package sent!")
                elif evt.data == b'\x02':
                    print("EVT TXDONE. Package confirmed!")
                print("Going to sleep ZzZz")
                self.state = State.READY
            elif evt.type == ModemDefs.EVT_DOWNDATA:
                print("EVT DOWNDATA")
                print(f"Got something: {evt.data}")

        return evt

    def run(self):
        self._get_state()
        print("Joining ...")
        while True:
            if self.state == State.INIT:
                self.m.join()
                self.state = State.JOINING
            elif self.state == State.JOINING:
                self._get_state()
            elif self.state == State.TRANSMITTING:
                self._get_state()
            elif self.state == State.READY:
                self._get_state()
                if self._clock == self._period:
                    self._clock = 0
                    self.m.tx(self._port, self.measure())
                    print("Sending data")
                    self.state = State.TRANSMITTING
                    print("Awaiting TX complete ...")
                else:
                    # sleeping
                    # the modem automatically goes to the lowest power consumption mode if no commands are issued
                    self._clock += 1


if __name__ == "__main__":
    ser_port = sys.argv[1] if len(sys.argv) == 2 else '/dev/ttyUSB0'

    app = Application(ser_port, period=15)

    try:
        app.run()
    except KeyboardInterrupt:
        print("bye")
