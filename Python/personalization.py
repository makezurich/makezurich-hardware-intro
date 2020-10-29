"""
Run it only once during comissioning, keys are persistent. 
"""
import sys
from modem import Modem

DEVEUI = 'FFFFFFAADC22E62A'
APPEUI = "70B3D57EF00037C8"
APPKEY = "732D3CF798E045E1537281860FE92217"

ser_port = sys.argv[1] if len(sys.argv) == 2 else '/dev/ttyUSB0'

m = Modem(ser_port)

m.setdeveui(bytes(bytearray.fromhex(DEVEUI)))
m.setjoineui(bytes(bytearray.fromhex(APPEUI)))
m.setnwkkey(bytes(bytearray.fromhex(APPKEY)))

assert m.euistr(m.deveui).replace('-','') == DEVEUI
assert m.euistr(m.joineui).replace('-','') == APPEUI 
