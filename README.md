# Nintendo Switch Controller Bot

Control your Nintendo switch using a Micro Controller Unit (MCU).
This setup focuses on having less necessary hardware and an easier setup.
Firmware uses Bluetooth to connect to the Console, while providing a Web Interface via WiFi for easy configuration.

This project utilizes a Real Time Operating System developed via the Zephyrproject.
The targeted board for this project is the ESP32.

## Getting Started

The following sections shall help you to get the project up and running on a Linux development environment.

### root: Install OS Dependencies

Please note that different distributions of Linux may have different system package managers with different package names. Therefore, here's a list of the packages needed. If you are unsure how to install and individual package on your OS, you may have a look [here](https://command-not-found.com/)

- `git`
- `cmake`
- `ninja`
- `gperf`
- `ccache`
- `dfu-util`
- `dtc`
- `wget`
- `python`
- `python-pip`
- `python-setuptools`
- `python-wheel`
- `python-tk`
- `xz`
- `file`
- `make`

### root: Modify User Permissions

Ensure the regular user belongs to all existing groups below to allow programming the devices without root permissions. (hint: `sudo usermod -aG <group> $USER`)
Note that you may need to reboot the OS in order to activate those effects.

- dialout
- tty
- uucp

### Setup Environment Variables

Ensure that the following environment variables are present on your system:

- `PATH` includes path to executables installed via python (typically `~/.local/bin`).
- `ESPRESSIF_TOOLCHAIN_PATH` = `${HOME}/.espressif/tools/zephyr`
- `ZEPHYR_TOOLCHAIN_VARIANT` = `espressif`

Restart your shell if necessary to apply changes here.

### Install `west` utility

`west` is Zephyr's build tool to interact with a Zephyrproject and can be installed via pip.
It is recommended that this installation is done with a non-root user.

```bash
python -m pip install --upgrade west
```

### Setup Zephyr Workspace

The following commands initialize a zephyr workspace and fetch other required sources.

```bash
west init -m https://github.com/dornbirndevelops/nintendo-switch-controller-mcu --mr rework/esp32-wireless-controller workspace
cd workspace
west update
```

### Setup Toolchain

The standard toolchain is recommended by Zephyr, whereas the Espressif toolchain and the submodules are necessary for the ESP32.

```bash
wget -O zephyr-sdk.run https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.13.2/zephyr-sdk-0.13.2-linux-x86_64-setup.run
chmod +x zephyr-sdk.run
./zephyr-sdk.run -- -d ~/zephyr-sdk-0.13.2
rm zephyr-sdk.run
```

```bash
west espressif install
west espressif update
```

### CMake exports & additional Python Dependencies

As a last preparation step, some CMake exports and python dependencies need to be available.

```bash
west zephyr-export
python -m pip install -r zephyr/scripts/requirements.txt
```

## Build, Flash

Once all previous steps are done, one can build and flash the custom application firmware.

```bash
west build -p auto -b esp32 nintendo-switch-controller-mcu/apps/hello_world
west flash
```
