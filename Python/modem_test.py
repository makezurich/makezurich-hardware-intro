# https://tamberg.mit-license.org/

import sys
from modem import Modem # Ask Diego or Gonzalo
from modem import CommandError
import modemdefs as ModemDefs
import time

devEui = "0000000000000000" # TODO
appEui = "0000000000000000" # TODO
appKey = "00000000000000000000000000000000" # TODO

# serialPort = '/dev/ttyUSB0' # Linux
serialPort = '/dev/tty.usbserial-M1V6V7' # MacOS: $ ls /dev/tty.u*

try:
	print("Setup...")
	m = Modem(serialPort)
	m.deveui = bytes(bytearray.fromhex(devEui))
	m.joineui = bytes(bytearray.fromhex(appEui))
	m.setnwkkey(bytes(bytearray.fromhex(appKey)))
	loraPort = 1 # valid values are 1 to 224
	loraPayload = b'hello'

	print("Joining...")
	m.join()
	event = None
	while (event == None) or (event.type != ModemDefs.EVT_JOINED):
		event = m.getevent()

	print("Joined :)")
	while True:
		try:
			print("Sending ", loraPayload)
			m.tx(loraPort, loraPayload)
			time.sleep(15) # seconds
		except Exception as e:
			e_type, e_obj, e_tb = sys.exc_info()
			print(e_type.__name__ + ":", e)
			time.sleep(3)

except Exception as e:
	e_type, e_obj, e_tb = sys.exc_info()
	print(e_type.__name__ + ":", e)
	print("Oops, un/replug the module and try again!")
