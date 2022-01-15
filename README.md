# Nintendo Switch Controller Bot

Control your Nintendo switch using a Micro Controller Unit (MCU).
This setup focuses on having less necessary hardware and an easier setup.
Firmware uses Bluetooth to connect to the Console, while providing a Web Interface via WiFi for easy configuration.

This project utilizes a Real Time Operating System developed via the Zephyrproject.
The targeted board for this project is the ESP32.

## Requirements

packages
- cmake
- python
- dtc (device tree compiler)
- git
- ninja
- west
- espressif toolchain

environment
- PATH += ~/.local/bin
- ZEPHYR_TOOLCHAIN_VARIANT = espressif
- ESPRESSIF_TOOLCHAIN_PATH = ~/.espressif/tools/zephyr

## Get Started

```bash
west init -m https://github.com/dornbirndevelops/nintendo-switch-controller-mcu --mr rework/esp32-wireless-controller nscws



cd nscws
west update
west zephyr-export
python -m pip install -r zephyr/scripts/requirements.txt

west build -b esp32 apps/hello_world
west flash
west espressif monitor
```
