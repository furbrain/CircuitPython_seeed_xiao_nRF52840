Introduction
============




.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/furbrain/CircuitPython_seeed_xiao_nRF52840/workflows/Build%20CI/badge.svg
    :target: https://github.com/furbrain/CircuitPython_seeed_xiao_nRF52840/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

Provides access to onboard sensors and battet


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Adafruit's LSM6DS library: <https://github.com/adafruit/Adafruit_CircuitPython_LSM6DS>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install seeed_xiao_nrf52840

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============


.. code-block:: python

    import array
    import time

    import audiocore
    import audiopwmio
    import board

    from seeed_xiao_nrf52840 import IMU, Mic, Battery

    with Battery() as bat:
        print(f"Charge_status: {bat.charge_status}")
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
            aud.play(sample,loop=True)
            print("playing")
            time.sleep(5)
            aud.stop()

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-seeed-xiao-nrf52840.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/furbrain/CircuitPython_seeed_xiao_nRF52840/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
