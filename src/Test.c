#include <avr/io.h>
#include <avr/wdt.h>
#include <avr/power.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>
#include <string.h>

#include <LUFA/Version.h>
#include <LUFA/Drivers/Board/LEDs.h>
#include <LUFA/Drivers/Peripheral/Serial.h>
#include <LUFA/Drivers/USB/USB.h>
#include <LUFA/Drivers/Board/Joystick.h>
#include <LUFA/Drivers/Board/LEDs.h>
#include <LUFA/Drivers/Board/Buttons.h>
#include <LUFA/Platform/Platform.h>

#include "LightweightRingBuff.h"

RingBuff_t USARTtoUSB_Buffer;

ISR(USART1_RX_vect, ISR_BLOCK)
{
	uint8_t ReceivedByte = UDR1;

	RingBuffer_Insert(&USARTtoUSB_Buffer, ReceivedByte);
}

// Configures hardware and peripherals, such as the USB peripherals.
void SetupHardware(void) {
	// We need to disable watchdog if enabled by bootloader/fuses.
	MCUSR &= ~(1 << WDRF);
	wdt_disable();

	// We need to disable clock division before initializing the USB hardware.
	clock_prescale_set(clock_div_1);

	// setup pull-up of RX
	PORTD |= _BV(PORTD2);

	// initialize serial port
	Serial_Init(9600, false);

    LEDs_Init();
}



// Main entry point.
int main(void) {
	// We'll start by performing hardware and peripheral setup.
	SetupHardware();

	RingBuffer_InitBuffer(&USARTtoUSB_Buffer);

    //unsigned char state = 0;

	// We'll then enable global interrupts for our use.
	GlobalInterruptEnable();
	// Once that's done, we'll enter an infinite loop.
	for (;;)
	{
		if (!RingBuffer_IsEmpty(&USARTtoUSB_Buffer)) {
            //state =
            RingBuffer_Remove(&USARTtoUSB_Buffer);
            LEDs_ToggleLEDs(LEDS_ALL_LEDS);
        }
	}
}
