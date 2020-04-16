# Nintendo Switch Controller Arduino

control your Nintendo Switch using an Arduino UNO R3

## Requirements

- Arduino Uno (R3)
- Tiny jumper cable (female female) to flash intermediate device chip
- USB cable
- Linux System like Ubuntu (Debian)

## Installation

### 1. clone repository

```
git clone --recursive git@github.com:dornbirndevelops/nintendo-switch-controller-arduino.git
```

### 2. install required packages

- AVR Compiler
- DFU Programmer (called FLIP on Windows):

```
sudo apt install gcc-avr avr-libc dfu-programmer
```

### 3. Build Flash (.hex) files for Arduino UNO R3 (atmega16u2)

```
make
```

## Flash

**IMPORTANT FOR NOTEBOOK USERS: [turn off autosuspend](https://unix.stackexchange.com/questions/91027/how-to-disable-usb-autosuspend-on-kernel-3-7-10-or-above) before flashing because dfu-programmer does not recognize your device otherwise. this change can be reverted afterwards.**

1. connect the Arduino UNO via USB Cable to your computer

2. verify that the Arduino gets discovered

```
lsusb
# Bus 001 Device 004: ID 2341:0043 Arduino SA Uno R3 (CDC ACM)
```

3. connect RESET to GND like in the image below **for about 1 second**:

![wiring](https://www.arduino.cc/en/uploads/Hacking/Uno-front-DFU-reset.png)

4. verify that the Arduino is now in DFU mode

```
lsusb
# Bus 001 Device 005: ID 03eb:2fef Atmel Corp.
```

5. decide, which .hex-file you want to flash onto your atmega16u2, few examples are below:

**default firmware**

```
sudo dfu-programmer atmega16u2 erase
sudo dfu-programmer atmega16u2 flash firmwares/Arduino-usbserial-atmega16u2-Uno-Rev3.hex
sudo dfu-programmer atmega16u2 reset
```

**spam-a** (just press a all the time in game)

```
sudo dfu-programmer atmega16u2 erase
sudo dfu-programmer atmega16u2 flash spam-a.hex
sudo dfu-programmer atmega16u2 reset
```

**any other firmware**

```
sudo dfu-programmer atmega16u2 erase
sudo dfu-programmer atmega16u2 flash path/to/firmware.hex
sudo dfu-programmer atmega16u2 reset
```

6. disconnect arduino from computer

## Usage

### Repeat A `spam-a.hex`

_spam-a just spams the A button. You can use it to farm Fossils at the Digging Duo and/or hunting Shiny (default) Fossils at Route 6_

1. go into the **Change Grip/Order** window on your Switch Homescreen and press nothing
2. plug in the Arduino UNO R3

### Watts Farm `wattsfarmer.hex`

1. walk to a den and throw an Wishing Piece in it
2. use the date spoofing exploit until the den glows red (don't go in yet!)
3. go into the **Change Grip/Order** window on your Switch Homescreen and press nothing
4. plug in the Arduino UNO R3

#### Masterballs `masterballs.hex`

_This uses the new VS date spamming exploit, look it up on youtube._

1. Enable the VS date spam exploit
2. go into a Pokécenter right in front of the computer
3. make sure you can play the lottery today (do not play yet)
4. set you switch clock settigns to manual mode
5. go into the **Change Grip/Order** window on your Switch Homescreen and press nothing
6. plug in the Arduino UNO R3

### Shiny breeding `wildareabreeding.hex` (NOT FULLY TESTED)

- open wildareabreeding.c in src folder
- change value at line 62 `#define cycles`to correct amount and save

1. fly to the daycare in the wild area
2. your party needs to be full and in the first slot should be a Pokémon with the **Flame Body** ability
3. selection in menu needs to hover the map button
4. exit the menu
5. go into the **Change Grip/Order** window on your Switch Homescreen and press nothing
6. plug in the Arduino UNO R3

### Farm Dracovish `dracovish.hex`

_make sure you have plenty of fossils in your inventory_

1. place yourself in front of the fossil lady.
2. go into the **Change Grip/Order** window on your Switch Homescreen and press nothing
3. plug in the Arduino UNO R3

### Release a full box of Pokémon `releasebox.hex`

_be careful using this_

1. open the box you want to release
2. go into the **Change Grip/Order** window on your Switch Homescreen and press nothing
3. plug in the Arduino UNO R3

## Thanks

Thanks to Shiny Quagsire for his [Splatoon post printer](https://github.com/shinyquagsire23/Switch-Fightstick) and progmem for his [original discovery](https://github.com/progmem/Switch-Fightstick).
Also thanks to bertrandom for his [snowball thrower](https://github.com/bertrandom/snowball-thrower) and all the modifications.
