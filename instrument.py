import pyvisa
import time

from utils import dbm_to_vpp

class SiglentSDG():
    def __init__(
        self,
        ipv4: str,
    ) -> None:

        rm = pyvisa.ResourceManager('@py')
        self.dev = rm.open_resource(f'TCPIP0::{ipv4}::inst0::INSTR')
        self.dev.write_termination = '\n'
        self.dev.read_termination = '\n'
        self.dev.query_delay = 1

        self.identification = self.query('*IDN?')

        # Reset instrument
        self.write('*RST')
        time.sleep(2)

        # Set screen saver
        self.write(f"SCSV 5MIN")

        # Enable external 10 MHz clock input
        self.write(f"ROSC EXT")

        # Configure output load channel 1 and 2
        self.write(f"C1:OUTP LOAD,50")
        self.write(f"C2:OUTP LOAD,50")

    def query(self, string: str):
        result = self.dev.query(string)
        return result

    def write(self, string: str) -> None:
        self.dev.write(string)

class Channel():
    def __init__(
        self,
        channel: int,
        combine: bool,
        hz: int,
        hz_shift: int,
        dbm: int,
        instrument,
    ) -> None:
        self.hz: int = hz
        self.hz_shift: int = hz_shift
        self.dbm: int = dbm
        self.vpp:float = dbm_to_vpp(dbm)
        self.channel: int = channel
        self.channel_str: str = f"C{channel}"

        self.instrument = instrument
        self.instrument.write(f"{self.channel_str}:CMBN {'ON' if combine else 'OFF'}")

    def fskcw(
        self,
    ) -> None:
        self.instrument.write(f"{self.channel_str}:MDWV STATE,ON")
        self.instrument.write(f"{self.channel_str}:MDWV FSK")
        self.instrument.write(f"{self.channel_str}:MDWV FSK,SRC,EXT")
        self.instrument.write(f"{self.channel_str}:MDWV FSK,HFRQ,{self.hz + self.hz_shift}")
        self.instrument.write(f"{self.channel_str}:MDWV CARR,WVTP,SINE")
        self.instrument.write(f"{self.channel_str}:MDWV CARR,FRQ,{self.hz}")
        self.instrument.write(f"{self.channel_str}:MDWV CARR,AMP,{self.vpp}")
        self.instrument.write(f"{self.channel_str}:MDWV CARR,OFST,0")
        self.instrument.write(f"{self.channel_str}:MDWV CARR,PHSE,0")

    def power(self, on: bool) -> None:
        state = "OFF"
        if on:
            state:str  = "ON"

        self.instrument.write(f"{self.channel_str}:OUTP {state}")
