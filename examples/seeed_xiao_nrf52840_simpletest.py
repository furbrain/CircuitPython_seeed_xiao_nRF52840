# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Phil Underwood for Underwood Underground
#
# SPDX-License-Identifier: Unlicense
import array
import time

import audiocore
import audiopwmio
import board

from seeed_xiao_nrf52840 import IMU, Mic, Battery

with Battery() as bat:
    print(f"Charge complete: {bat.charge_status}")
    print(f"Voltage: {bat.voltage}")
    print(f"Charge_current high?: {bat.charge_current}")
    print("Setting charge current to high")
    bat.charge_current = bat.CHARGE_100MA
    print(f"Charge_current high?: {bat.charge_current}")

with IMU() as imu:
    for i in range(5):
        print("Acceleration:", imu.acceleration)
        time.sleep(1)

with Mic() as mic:
    for i in range(5):
        print(f"Start speaking in: {5-i}")
        time.sleep(1)
    b = array.array("H")
    for i in range(8000):
        b.append(0)
    print("SPEAK!!!")
    mic.record(b, len(b))
    print(b)
    for i in range(5):
        print(f"Replaying in: {5-i}")
        time.sleep(1)
    with audiopwmio.PWMAudioOut(board.D0) as aud:
        print("PWM setup")
        sample = audiocore.RawSample(b, sample_rate=8000)
        print("sample ready")
        aud.play(sample, loop=True)
        print("playing")
        time.sleep(5)
        aud.stop()
