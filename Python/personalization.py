"""
Copyright (C) Gonzalo Casas 2020
Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).

Run it only once during comissioning, keys are persistent. 
"""
import sys
from modem import Modem

DEVEUI = 'REPLACEME'
APPEUI = "REPLACEME"
APPKEY = "REPLACEME"

ser_port = sys.argv[1] if len(sys.argv) == 2 else '/dev/ttyUSB0'

m = Modem(ser_port)

m.setdeveui(bytes(bytearray.fromhex(DEVEUI)))
m.setjoineui(bytes(bytearray.fromhex(APPEUI)))
m.setnwkkey(bytes(bytearray.fromhex(APPKEY)))

assert m.euistr(m.deveui).replace('-','') == DEVEUI
assert m.euistr(m.joineui).replace('-','') == APPEUI 
