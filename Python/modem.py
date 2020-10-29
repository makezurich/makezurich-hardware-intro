"""
Copyright (C) Gonzalo Casas 2020
Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
"""

#
# Utility class to exchange commands with modem connected via serial port (e.g. FTDI Serial-to-USB adapter).
#
# Next to the TXD/RXD lines of the serial port, the RTS/CTS lines
# are used to drive the modem's COMMAND and BUSY pins:
#
#  MODEM GPIO SERIAL FTDI
#  ----- ---- ------ ------
#  RX    PA10 TXD    orange
#  TX    PA9  RXD    yellow
#  CMD   PB8  RTS    green
#  BUSY  PA8  CTS    brown
#  GND        GND    black
#

from typing import List, Optional, Tuple, Union

import sys
import time
import string
from serial import Serial
from struct import pack, unpack, unpack_from
from binascii import crc32
from datetime import datetime, timedelta

import modemdefs as ModemDefs


class CommandError(Exception):

    rcnames  = { v:n[3:] for n,v in vars(ModemDefs).items() if n.startswith('RC_') }

    def __init__(self, rc):
        self.rc = rc

    def __str__(self):
        return 'command failed ' + CommandError.rcnames.get(self.rc, str(self.rc))


class Event:
    def __init__(self, ev:Tuple):
        self.type = ev[0]
        self.cnt  = ev[1]
        self.data = ev[2]
    def __str__(self):
        if self.type == ModemDefs.EVT_RESET:
            return 'RESET: counter=%d' % unpack('>H', self.data)
        elif self.type == ModemDefs.EVT_TXDONE:
            return 'TXDONE: ' + { 0x00: 'frame not sent', 0x01: 'frame sent', 0x02: 'frame sent and confirmed'}.get(self.data[0])
        elif self.type == ModemDefs.EVT_DOWNDATA:
            (rssi, snr, flags, port) = unpack_from('bbBB', self.data)
            return 'DOWNDATA: RSSI=%ddBm, SNR=%ddB, flags=%02x, port=%d, payload=%s' % (rssi-64, snr*0.25, flags, port, self.data[4:].hex())
        elif self.type == ModemDefs.EVT_UPLOADDONE:
            return 'UPLOADDONE: ' + ('successfully completed' if self.data[0] == 0x01 else 'aborted')
        elif self.type == ModemDefs.EVT_LINKSTATUS:
            return 'LINKSTATUS: ' + ('connection active' if self.data[0] == 0x01 else 'connection inactive')
        elif self.type == ModemDefs.EVT_JOINED:
            return 'JOINED'
        elif self.type == ModemDefs.EVT_JOINFAIL:
            return 'JOINFAIL'
        elif self.type == ModemDefs.EVT_STREAMDONE:
            return 'STREAMDONE'
        elif self.type == ModemDefs.EVT_ALARM:
            return 'ALARM'
        else:
            return 'type=%d, count=%d, data=%s' % (self.type, self.cnt, self.data.hex())


class Modem:

    # names for constants from ModemDefs
    evnames   = { v:n[4:] for n,v in vars(ModemDefs).items() if n.startswith('EVT_') }
    infnames  = { v:n[4:] for n,v in vars(ModemDefs).items() if n.startswith('INF_') }
    adrnames  = { v:n[5:] for n,v in vars(ModemDefs).items() if n.startswith('ADRP_') }
    statnames = { v:n[5:] for n,v in vars(ModemDefs).items() if n.startswith('STAT_') }
    regnames  = { 1: 'EU868', 2: 'AS923', 3: 'US915', 4: 'AU915', 5: 'CN470' }

    # return EUI string
    @staticmethod
    def euistr(euidata:bytes) -> str:
        return "-".join(["{:02X}".format(x) for x in euidata])

    # get bytes from filename / bytearray / bytes
    @staticmethod
    def getbytes(data:Union[str,bytes,bytearray]) -> bytes:
        if isinstance(data, str):
            with open(data, 'rb') as f:
                return f.read()
        elif isinstance(data, bytes):
            return data
        elif isinstance(data, bytearray):
            return bytes(data)
        else:
            raise ValueError('data must be filename / bytearray / bytes')

    @staticmethod
    def lrc(buf:bytes) -> int:
        lrc = 0
        for x in buf:
            lrc ^= x
        return lrc

    @staticmethod
    def make_packet(cmd:int, payload:bytes=b'') -> bytes:
        # command: CMD[1] LEN[1] DATA[...] LRC[1]
        pkt = bytes([cmd, len(payload)]) + payload
        return pkt + bytes([Modem.lrc(pkt)])

    def __init__(self, port:str='/dev/ttyUSB0'):
        # open modem interface (open after setting rts)
        self.ser = Serial(baudrate=115200, timeout=1, inter_byte_timeout=0.010, rtscts=True)
        self.ser.port = port
        self.ser.rts = 0
        self.ser.open()

    def __exit__(self, *exc) -> None:
        self.ser.close()

    def __str__(self):
        (bl, fw, lw) = m.version
        s  = 'bootloader:   %X\n' % bl
        s += 'firmware:     %08X\n' % fw
        s += 'LoRaWAN:      %d.%d.%d\n' % ((lw >> 8) & 0xF, (lw >> 4) & 0xF, lw & 0xF)
        s += 'PIN:          %s\n' % m.pin.hex().upper()
        s += 'chipeui:      %s\n' % Modem.euistr(m.chipeui)
        s += 'deveui:       %s\n' % Modem.euistr(m.deveui)
        s += 'joineui:      %s\n' % Modem.euistr(m.joineui)
        s += 'region:       %s\n' % Modem.regnames[m.region]
        s += 'regionlist:   %s\n' % ' '.join([Modem.regnames[x] for x in m.regionlist])
        s += 'TXpowoff:     %d dB\n' % m.txpowoff
        s += 'ADR profile:  %s\n' % Modem.adrnames[m.profile]
        s += 'DM interval:  %ds\n' % m.interval
        s += 'DM port:      %d\n' % m.dmport
        s += 'DM fields:    %s\n' % ' '.join([Modem.infnames[x].lower() for x in m.dmfields])
        trace = m.gettrace()
        if trace:
            s += 'backtrace:    %s\n' % trace.hex()
        s += 'charge:       %d mAh\n' % m.getcharge()
        stat = m.getstatus()
        s += 'status:       %s\n' % ' '.join([Modem.statnames[1 << x] for x in range(8) if stat & (1 << x) != 0])
        return s

    def send_packet(self, pkt):
        # assert COMMAND line (active-low)
        self.ser.rts = True
        # wait until BUSY goes low (active-high, max 10ms)
        t0 = time.time()
        while self.ser.cts == False:
            assert (time.time() - t0 < 0.010), "timeout waiting for BUSY line going low"
        # send packet
        self.ser.write(pkt)
        # (ser.flush() not working)
        time.sleep(0.025)
        # de-assert COMMAND line
        self.ser.rts = False

    # response: RC[1] LEN[1] DATA[...] LRC[1] --> (rc, data)
    def read_packet(self) -> Optional[Tuple]:
        buf = bytearray()
        while len(buf) < 3 or len(buf) < 3 + buf[1]:
            b = self.ser.read()
            if len(b) != 1:
                break
            buf += b
        return (buf[0], bytes(buf[2:-1])) if len(buf) >= 3 and len(buf) == 3 + buf[1] and Modem.lrc(buf) == 0 else None

    # send command / receive response
    def command(self, cmd:int, payload:bytes=b'') -> bytes:
        # send command packet
        self.send_packet(Modem.make_packet(cmd, payload))
        # read response packet
        rsp = self.read_packet()
        # check response
        if not rsp:
            raise CommandError(ModemDefs.RC_FRAMEERROR)
        if rsp[0] != ModemDefs.RC_OK:
            raise CommandError(rsp[0])
        return rsp[1] # -> data

    # modem commands...

    def getversion(self) -> Tuple:
        data = self.command(ModemDefs.CMD_GETVERSION)
        return unpack('>IIH', data) # -> (bl, fw, lw)

    def getpin(self) -> bytes:
        pin = self.command(ModemDefs.CMD_GETPIN)
        return pin

    def getchipeui(self) -> bytes:
        chipeui = self.command(ModemDefs.CMD_GETCHIPEUI)
        return chipeui

    def getdeveui(self) -> bytes:
        deveui = self.command(ModemDefs.CMD_GETDEVEUI)
        return deveui

    def setdeveui(self, eui:bytes):
        if not isinstance(eui, bytes) or len(eui) != 8:
            raise ValueError('deveui must be 8 bytes')
        self.command(ModemDefs.CMD_SETDEVEUI, eui)

    def getjoineui(self) -> bytes:
        joineui = self.command(ModemDefs.CMD_GETJOINEUI)
        return joineui

    def setjoineui(self, joineui:bytes):
        if not isinstance(joineui, bytes) or len(joineui) != 8:
            raise ValueError('joineui must be 8 bytes')
        self.command(ModemDefs.CMD_SETJOINEUI, joineui)

    def setnwkkey(self, key:bytes):
        if not isinstance(key, bytes) or len(key) != 16:
            raise ValueError('nwkkey must be 16 bytes')
        self.command(ModemDefs.CMD_SETNWKKEY, key)

    def getregion(self) -> int:
        region = self.command(ModemDefs.CMD_GETREGION)
        return region[0]

    def setregion(self, regcode:int):
        self.command(ModemDefs.CMD_SETREGION, bytes([regcode]))

    def listregions(self) -> Tuple:
        regions = self.command(ModemDefs.CMD_LISTREGIONS)
        return unpack('B' * len(regions), regions)

    def gettxpowoff(self) -> int:
        txpowoff = self.command(ModemDefs.CMD_GETTXPOWEROFFSET)
        return unpack('b', txpowoff)[0]

    def settxpowoff(self, off:int):
        self.command(ModemDefs.CMD_SETTXPOWEROFFSET, pack('b', off))

    def getprofile(self) -> int:
        profile = self.command(ModemDefs.CMD_GETADRPROFILE)
        return profile[0]

    def setprofile(self, pro:int, custom=b''):
        if not ((pro >= 0 and pro < 3 and len(custom) == 0) or (pro == 3 and len(custom) == 16)):
            raise ValueError('profile must be 0-2 without data, or 3 with 16 bytes custom data rates')
        self.command(ModemDefs.CMD_SETADRPROFILE, bytes([pro]) + custom)

    def getinterval(self) -> int:
        data = self.command(ModemDefs.CMD_GETDMINFOINTERVAL)
        return (data[0] & 0x3F) * ((1, 60*60*24, 60*60, 60)[data[0] >> 6])

    def setinterval(self, val:int, unit='s'):
        if val > 63:
            raise ValueError('value out of range 0-63: ' + str(val))
        self.command(ModemDefs.CMD_SETDMINFOINTERVAL, bytes([((ord(unit) << 4) & 0xC0) | val]))

    def getdmport(self) -> int:
        dmport = self.command(ModemDefs.CMD_GETDMPORT)
        return dmport[0]

    def setdmport(self, port:int):
        self.command(ModemDefs.CMD_SETDMPORT, bytes([port]))

    def getdmfields(self) -> Tuple:
        fields = self.command(ModemDefs.CMD_GETDMINFOFIELDS)
        return unpack('B' * len(fields), fields)

    def setdmfields(self, fields:bytes):
        self.command(ModemDefs.CMD_SETDMINFOFIELDS, fields)

    def gettrace(self):
        trace = self.command(ModemDefs.CMD_GETTRACE)
        return trace if len(trace) > 0 else None

    def getstatus(self) -> int:
        data = self.command(ModemDefs.CMD_GETSTATUS)
        return data[0]

    def getevent(self):
        data = self.command(ModemDefs.CMD_GETEVENT)
        return (Event((data[0], data[1], data[2:])) if len(data) > 0 else None) # -> (evtype, cnt, data)

    def getcharge(self) -> int:
        charge = self.command(ModemDefs.CMD_GETCHARGE)
        return unpack('>I', charge)[0] # -> mAh

    def reset(self):
        self.command(ModemDefs.CMD_RESET)

    def factory(self):
        self.command(ModemDefs.CMD_FACTORYRESET)

    def resetcharge(self):
        self.command(ModemDefs.CMD_RESETCHARGE)

    def setalarm(self, seconds:int):
        self.command(ModemDefs.CMD_SETALARM, pack('>I', seconds))

    def firmwareupdate(self, blockno, blockcnt, blockdata):
        if blockno >= blockcnt:
            raise ValueError('blockno must be less than blockcnt')
        if len(blockdata) > 128 or (blockno != blockcnt-1 and len(blockdata) != 128):
            raise ValueError('size of blockdata must be 128 for all but the last block')
        self.command(ModemDefs.CMD_FIRMWAREUPDATE, pack('>HH', blockno, blockcnt) + blockdata)

    def join(self):
        self.command(ModemDefs.CMD_JOIN)

    def leave(self):
        self.command(ModemDefs.CMD_LEAVENETWORK)

    def suspend(self, susp:bool):
        self.command(ModemDefs.CMD_SUSPENDMODEMCOMM, bytes([0x01 if susp else 0x00]))

    def maxpayload(self) -> int:
        size = self.command(ModemDefs.CMD_GETNEXTTXMAXPAYLOAD)
        return size[0]

    def requesttx(self, port:int, payload:bytes, confirmed=False):
        self.command(ModemDefs.CMD_REQUESTTX, bytes([port, 0x01 if confirmed else 0x00]) + payload)

    def emergencytx(self, port:int, payload:bytes, confirmed=False):
        self.command(ModemDefs.CMD_EMERGENCYTX, bytes([port, 0x01 if confirmed else 0x00]) + payload)

    def gettime(self) -> int:
        seconds = self.command(ModemDefs.CMD_GETTIME)
        return unpack('>I', seconds)[0]

    def getclass(self) -> int:
        cls = self.command(ModemDefs.CMD_GETCLASS)
        return cls[0]

    def setclass(self, cl:int):
        self.command(ModemDefs.CMD_SETCLASS, bytes([cl]))

    def setmulticast(self, grpaddr, nwkkeydn, appkey, seqnoadn):
        if not (isinstance(nwkkeydn, bytes) and len(nwkkeydn) == 16 and isinstance(appkey, bytes) and len(appkey) == 16):
            raise ValueError('session keys must be 16 bytes')
        self.command(ModemDefs.CMD_SETMULTICAST, pack('>I', grpaddr) + nwkkeydn + appkey + pack('>I', seqnoadn))

    def uploadinit(self, port:int, enc:bool, size:int, delay:int):
        self.command(ModemDefs.CMD_UPLOADINIT, pack('>BBHH', port, 0x01 if enc else 0x00, size, delay))

    def uploaddata(self, data:bytes):
        self.command(ModemDefs.CMD_UPLOADDATA, data)

    def uploadstart(self, crc:int):
        self.command(ModemDefs.CMD_UPLOADSTART, pack('>I', crc))

    def senddmstatus(self, fields:bytes):
        self.command(ModemDefs.CMD_SENDDMSTATUS, fields)

    def setappstatus(self, status:bytes):
        if not isinstance(status, bytes) or len(status) != 8:
            raise ValueError('appstatus must be 8 bytes')
        self.command(ModemDefs.CMD_SETAPPSTATUS, status)

    def streaminit(self, port:int, enc:bool):
        self.command(ModemDefs.CMD_STREAMINIT, bytes([port, 0x01 if enc else 0x00]))

    def streamdata(self, port:int, record:bytes):
        self.command(ModemDefs.CMD_SENDSTREAMDATA, bytes([port]) + record)

    def streamstatus(self, port:int) -> Tuple:
        stat = self.command(ModemDefs.CMD_STREAMSTATUS, bytes([port]))
        return unpack('>HH', stat) # -> (pending, free)

    # convenience methods...

    def tx(self, port:int, payload:bytes, emergency=False, confirmed=False):
        self.command(ModemDefs.CMD_EMERGENCYTX if emergency else ModemDefs.CMD_REQUESTTX,
                     bytes([port, 0x01 if confirmed else 0x00]) + payload)

    def update(self, data):
        data = Modem.getbytes(data)
        blkcnt = (len(data) + 127) // 128
        for blkno in range(blkcnt):
            self.firmwareupdate(blkno, blkcnt, data[block*128:(block+1)*128])

    def upload(self, port:int, data, enc=False, delay=5):
        data = Modem.getbytes(data)
        self.uploadinit(port, enc, len(data), delay)
        for x in range(0, len(data), 128):
            self.uploaddata(data[x:x+128])
        self.uploadstart(crc32(data))

    # accessor methods for static, perso and config data...

    @property
    def version(self):
        return self.getversion()

    @property
    def pin(self):
        return self.getpin()

    @property
    def chipeui(self):
        return self.getchipeui()

    @property
    def deveui(self):
        return self.getdeveui()

    @deveui.setter
    def deveui(self, eui):
        self.setdeveui(eui)

    @property
    def joineui(self):
        return self.getjoineui()

    @joineui.setter
    def joineui(self, eui):
        self.setjoineui(eui)

    @property
    def nwkkey(self):
        raise AttributeError('nwkkey can only be set, not read')

    @nwkkey.setter
    def nwkkey(self, key):
        self.setnwkkey(key)

    @property
    def region(self):
        return self.getregion()

    @region.setter
    def region(self, regcode):
        return self.setregion(regcode)

    @property
    def regionlist(self):
        return self.listregions()

    @property
    def txpowoff(self):
        return self.gettxpowoff()

    @txpowoff.setter
    def txpowoff(self, off):
        return self.settxpowoff(off)

    @property
    def interval(self):
        return self.getinterval()

    @interval.setter
    def interval(self, sec):
        if sec < 63:
            val = sec
            unit = 's'
        elif sec < 60*60:
            val = sec // 60
            unit = 'm'
        elif sec < 60*60*24:
            val = sec // (60*60)
            unit = 'h'
        else:
            val = sec // (60*60*24)
            unit = 'd'
        self.setinterval(val, unit)

    @property
    def dmport(self):
        return self.getdmport()

    @dmport.setter
    def dmport(self, port):
        self.setdmport(port)

    @property
    def dmfields(self):
        return self.getdmfields()

    @dmfields.setter
    def dmfields(self, port):
        self.setdmfields(port)

    @property
    def profile(self):
        return self.getprofile()

    @profile.setter
    def profile(self, pro):
        if pro == ModemDefs.ADRP_CUSTOM:
            raise ValueError('custom ADR profile an only be set via setprofile() method')
        return self.setprofile(pro)


if __name__ == '__main__':
    # select serial port
    port = sys.argv[1] if len(sys.argv) == 2 else '/dev/ttyUSB0'

    # create modem
    m = Modem(port)

    # print info
    print(m)
