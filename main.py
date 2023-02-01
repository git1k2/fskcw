import croniter
import datetime
import logging
import signal
import sys
import pause

from gpiozero import DigitalOutputDevice
from rich.logging import RichHandler
from rich.progress import track
from rich.table import Table
from time import sleep
from typing import Type

from morse import Morse
from instrument import (
    Channel,
    SiglentSDG
)

import config

def main() -> None:

    def signal_handler(signum, frame):
        for channel in channels:
            print(f"Power off channel {channel.channel}...")
            channel.power(on=False)
        sys.exit(1)

    FORMAT = "%(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler()]
    )
    log = logging.getLogger("rich")

    # Setup instrument
    instrument: SiglentSDG = SiglentSDG(ipv4=config.ipv4)
    channels: list[Channel] = [
        Channel(
            channel=1,
            combine=True,
            hz=7039810,
            hz_shift=5,
            dbm=10,
            instrument=instrument
        ),
        Channel(
            channel=2,
            combine=False,
            hz=14096870,
            hz_shift=5,
            dbm=10,
            instrument=instrument
        )
    ]
    signal.signal(signal.SIGINT, signal_handler)

    # Configure FSKCW modulation
    for channel in channels:
        channel.fskcw()

    # Setup Morse 
    trigger = DigitalOutputDevice(
        12,
        active_high=True
    )
    morse: Morse = Morse(
        text = " pa2st ",
    )

    # Seconds per dit
    dit_secs: float = 6

    # Length of frame in minutes
    frame_minutes: int = 10

    tx_length: int = round(len(morse.ook_timing) * dit_secs)
    if len(morse.ook_timing) * dit_secs > (frame_minutes * 60):
        log.error(f"Transmission duration ({tx_length} sec.) would be longer than a {frame_minutes} minute frame!")
        sys.exit(1)

    log.info(f"Connected device: {instrument.identification}")

    for channel in channels:
        log.info(
            f"Channel: {channel.channel}, "
            f"frequency: {channel.hz}, "
            f"shift: {channel.hz_shift}, "
            f"power: {channel.dbm} dBm / {channel.vpp} Vpp"
        )  

    now = datetime.datetime.now()
    sched: str  = f'1/{frame_minutes} * * * *'
    cron = croniter.croniter(sched, now)

    while True:
        nextdate = cron.get_next(datetime.datetime)
        log.info(f"Waiting for next transmission: {nextdate}")
        pause.until(nextdate)

        print(f"Sending text: '{morse.text.replace(' ', '_')}'")
        channels[0].power(on=True)
        for i in track(morse.ook_timing, description="Transmitting..."):
            if i == 0:
                trigger.off()
            if i == 1:
                trigger.on()
            sleep(dit_secs)
        channels[0].power(on=False)

if __name__ == "__main__":
    main()
