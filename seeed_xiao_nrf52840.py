# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Phil Underwood for Underwood Underground
#
# SPDX-License-Identifier: MIT
"""
`seeed_xiao_nrf52840`
================================================================================

Provides access to onboard battery management (and accelerometer and microphone for
the Sense model)


* Author(s): Phil Underwood

Implementation Notes
--------------------

**Hardware:**

* `Seeed Xiao nRF52840 (Sense)
  <https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

* Adafruit's LSM6DS library: https://github.com/adafruit/Adafruit_CircuitPython_LSM6DS
"""
import time

import analogio

# imports
import board
import busio
import digitalio
from audiobusio import PDMIn

from adafruit_lsm6ds.lsm6ds3 import LSM6DS3


class IMU(LSM6DS3):
    """
    IMU on Seeed XIAO nRF52840 Sense (only available on Sense models).
    This is an LSM6DS3 chip, and provides accelerometer and gyro readings
    """

    def __init__(self):
        # turn on IMU
        self.pwr_pin = digitalio.DigitalInOut(board.IMU_PWR)
        self.pwr_pin.direction = digitalio.Direction.OUTPUT
        self.pwr_pin.value = True

        # set up i2c
        self.i2c_bus = busio.I2C(board.IMU_SCL, board.IMU_SDA)
        time.sleep(
            0.05
        )  # wait 50ms for device to turn on (datasheet states typical 35ms)

        # finally initialise self
        super().__init__(self.i2c_bus, address=0x6A)

    def deinit(self) -> None:
        """
        Turn off device and release resources
        """
        self.pwr_pin.value = False
        self.pwr_pin.deinit()
        self.i2c_bus.deinit()


class Mic(PDMIn):
    """
    On-board  Microphone for Seeed XIAO nRF52840 Sense. Only available on Sense
    boards
    """

    def __init__(self, sample_rate, bit_depth):
        self.pwr_pin = digitalio.DigitalInOut(board.MIC_PWR)
        self.pwr_pin.direction = digitalio.Direction.OUTPUT
        self.pwr_pin.value = True

        super().__init__(sample_rate, bit_depth)

    def deinit(self):
        """
        Turn off the Microphone and release all resources
        """
        super().deinit()
        self.pwr_pin.value = False
        self.pwr_pin.deinit()


class Battery:
    """
    Seeed XIAO nRF52840 battery management functions
    """

    CHARGE_50MA: int = 0
    CHARGE_100MA: int = 1

    def __init__(self):
        self._charge_status = digitalio.DigitalInOut(board.CHARGE_STATUS)
        self._charge_status.direction = digitalio.Direction.INPUT
        self._charge_status.pull = digitalio.Pull.UP

        self._charge_speed = digitalio.DigitalInOut(board.P0_17)
        self._charge_speed.direction = digitalio.Direction.INPUT

        self._read_batt_enable = digitalio.DigitalInOut(board.READ_BATT_ENABLE)
        self._read_batt_enable.direction = digitalio.Direction.INPUT

        self._vbat = analogio.AnalogIn(board.VBATT)

    @property
    def charge_status(self) -> bool:
        """
        Battery charge status; `True` if Battery fully charged, `False` otherwise
        """
        return not self._charge_status.value

    @property
    def voltage(self) -> float:
        """
        Battery voltage in volts
        """
        # set READ_BATT_ENABLE to sink to allow voltage reading
        self._read_batt_enable.direction = digitalio.Direction.OUTPUT
        self._read_batt_enable.value = False
        # wait a little bit to allow voltage to settle
        time.sleep(0.003)
        value = (self._vbat.value / 65535.0) * self._vbat.reference_voltage * 2
        self._read_batt_enable.direction = digitalio.Direction.INPUT
        return value

    @property
    def charge_current(self) -> int:
        """
        Battery charge current, either Battery.CHARGE_50MA or Battery.CHARGE_100MA
        """
        if self._charge_speed.direction == digitalio.Direction.INPUT:
            return self.CHARGE_50MA
        return self.CHARGE_100MA

    @charge_current.setter
    def charge_current(self, value: int):
        if value == self.CHARGE_50MA:
            self._charge_speed.direction = digitalio.Direction.INPUT
        elif value == self.CHARGE_100MA:
            self._charge_speed.direction = digitalio.Direction.OUTPUT
            self._charge_speed.value = False
        else:
            raise ValueError("value must be either CHARGE_50MA or CHARGE_100MA")

    def deinit(self) -> None:
        """
        Release all resources
        """
        self._charge_status.deinit()
        self._charge_speed.deinit()
        self._read_batt_enable.deinit()
        self._vbat.deinit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deinit()


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/furbrain/CircuitPython_seeed_xiao_nRF52840.git"
