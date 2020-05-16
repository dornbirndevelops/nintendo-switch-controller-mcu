/**
 * IMPORTANT!
 * WHEN wiring the Arduino Uno R3 board,
 * the TX and RX ports connected to the atmega16u2
 * are switched since it is meant to be a middleman!!
 *
 * This means (from the atmega16u2 perspective):
 * - Board Pin TX -> 1 = atmega16u2 Receive Pin
 * - Board Pin RX <- 0 = atmega16u2 Transmit Pin
 *
 * in case you want to have the right pin configuration,
 * write a simple Arduino Program for the ATmega328P
 * working as a Serial bridge.
 */

#include "Joystick.h"

#include <stdint.h>
#include <stdbool.h>

#include <avr/io.h>
#include <avr/interrupt.h>

#include <util/delay.h>

#include <LUFA/Drivers/Peripheral/Serial.h>
#include <LUFA/Drivers/Board/LEDs.h>

#include "LightweightRingBuff.h"

// initial state is no buttons pressed
volatile USB_JoystickReport_Input_t commands[2] = {
	{.Button = 0,
	 .DPAD = DPAD_CENTER,
	 .LX = STICK_CENTER,
	 .LY = STICK_CENTER,
	 .RX = STICK_CENTER,
	 .RY = STICK_CENTER,
	 .VendorSpec = 0},
	{.Button = 0,
	 .DPAD = DPAD_CENTER,
	 .LX = STICK_CENTER,
	 .LY = STICK_CENTER,
	 .RX = STICK_CENTER,
	 .RY = STICK_CENTER,
	 .VendorSpec = 0}};
volatile unsigned char command_used = 0;

#define COMMAND_USED commands[command_used]
#define COMMAND_UNUSED commands[command_used ^ 1]

RingBuff_t RX_Buffer;

void updateCommands()
{
	static volatile unsigned char command_idx = 0;
	// update the controller input if new data is available in buffer
	volatile unsigned char data;

	volatile RingBuff_Count_t BufferCount = RingBuffer_GetCount(&RX_Buffer);
	while (BufferCount--)
	{
		data = RingBuffer_Remove(&RX_Buffer);
		// put new partial command into the build
		switch (command_idx++)
		{
		case 0:
			COMMAND_UNUSED.Button = data;
			COMMAND_UNUSED.Button <<= 8;
			break;
		case 1:
			COMMAND_UNUSED.Button |= data;
			break;
		case 2:
			COMMAND_UNUSED.DPAD = data;
			break;
		case 3:
			COMMAND_UNUSED.LX = data;
			break;
		case 4:
			COMMAND_UNUSED.LY = data;
			break;
		case 5:
			COMMAND_UNUSED.RX = data;
			break;
		case 6:
			COMMAND_UNUSED.RY = data;
			break;
		case 7:
			COMMAND_UNUSED.VendorSpec = data;
			// last field is filled now.
			// switch active commands
			command_used ^= 1;
			// reset idx so new command can be received
			command_idx = 0;
			break;
		default:
			break;
		}
	}
}

// Main entry point.
int main(void)
{
	// We'll start by performing hardware and peripheral setup.
	SetupHardware();

	// Initialize Buffer
	RingBuffer_InitBuffer(&RX_Buffer);

	// We'll then enable global interrupts for our use.
	GlobalInterruptEnable();
	// Once that's done, we'll enter an infinite loop.
	for (;;)
	{
		// We need to run our task to process and deliver data for our IN and OUT endpoints.
		HID_Task();
		// We also need to run the main USB management task.
		USB_USBTask();
	}
}

// Configures hardware and peripherals, such as the USB peripherals.
void SetupHardware(void)
{
	// We need to disable watchdog if enabled by bootloader/fuses.
	MCUSR &= ~(1 << WDRF);
	wdt_disable();

	// We need to disable clock division before initializing the USB hardware.
	clock_prescale_set(clock_div_1);
	// We can then initialize our hardware and peripherals, including the USB stack.

	// initialize serial port with interrupts
	Serial_Init(9600, false);
	UCSR1B |= (1 << RXCIE1);

#ifdef ALERT_WHEN_DONE
// Both PORTD and PORTB will be used for the optional LED flashing and buzzer.
#warning LED and Buzzer functionality enabled. All pins on both PORTB and PORTD will toggle when printing is done.
	DDRD = 0xFF; //Teensy uses PORTD
	PORTD = 0x0;
	//We'll just flash all pins on both ports since the UNO R3
	DDRB = 0xFF; //uses PORTB. Micro can use either or, but both give us 2 LEDs
	PORTB = 0x0; //The ATmega328P on the UNO will be resetting, so unplug it?
#endif
	// The USB stack should be initialized last.
	USB_Init();
}

// Fired to indicate that the device is enumerating.
void EVENT_USB_Device_Connect(void)
{
	// We can indicate that we're enumerating here (via status LEDs, sound, etc.).
}

// Fired to indicate that the device is no longer connected to a host.
void EVENT_USB_Device_Disconnect(void)
{
	// We can indicate that our device is not ready (via status LEDs, sound, etc.).
}

// Fired when the host set the current configuration of the USB device after enumeration.
void EVENT_USB_Device_ConfigurationChanged(void)
{
	bool ConfigSuccess = true;

	// We setup the HID report endpoints.
	ConfigSuccess &= Endpoint_ConfigureEndpoint(JOYSTICK_OUT_EPADDR, EP_TYPE_INTERRUPT, JOYSTICK_EPSIZE, 1);
	ConfigSuccess &= Endpoint_ConfigureEndpoint(JOYSTICK_IN_EPADDR, EP_TYPE_INTERRUPT, JOYSTICK_EPSIZE, 1);

	// We can read ConfigSuccess to indicate a success or failure at this point.
}

// Process control requests sent to the device from the USB host.
void EVENT_USB_Device_ControlRequest(void)
{
	// We can handle two control requests: a GetReport and a SetReport.

	// Not used here, it looks like we don't receive control request from the Switch.
}

// Process and deliver data from IN and OUT endpoints.
void HID_Task(void)
{
	// If the device isn't connected and properly configured, we can't do anything here.
	if (USB_DeviceState != DEVICE_STATE_Configured)
		return;

	// We'll start with the OUT endpoint.
	Endpoint_SelectEndpoint(JOYSTICK_OUT_EPADDR);
	// We'll check to see if we received something on the OUT endpoint.
	if (Endpoint_IsOUTReceived())
	{
		// If we did, and the packet has data, we'll react to it.
		if (Endpoint_IsReadWriteAllowed())
		{
			// We'll create a place to store our data received from the host.
			USB_JoystickReport_Output_t JoystickOutputData;
			// We'll then take in that data, setting it up in our storage.
			while (Endpoint_Read_Stream_LE(&JoystickOutputData, sizeof(JoystickOutputData), NULL) != ENDPOINT_RWSTREAM_NoError)
				;
			// At this point, we can react to this data.

			// However, since we're not doing anything with this data, we abandon it.
		}
		// Regardless of whether we reacted to the data, we acknowledge an OUT packet on this endpoint.
		Endpoint_ClearOUT();
	}

	// We'll then move on to the IN endpoint.
	Endpoint_SelectEndpoint(JOYSTICK_IN_EPADDR);
	// We first check to see if the host is ready to accept data.
	if (Endpoint_IsINReady())
	{
		// We'll create an empty report.
		USB_JoystickReport_Input_t JoystickInputData;
		// We'll then populate this report with what we want to send to the host.
		GetNextReport(&JoystickInputData);
		// Once populated, we can output this data to the host. We do this by first writing the data to the control stream.
		while (Endpoint_Write_Stream_LE(&JoystickInputData, sizeof(JoystickInputData), NULL) != ENDPOINT_RWSTREAM_NoError)
			;
		// We then send an IN packet on this endpoint.
		Endpoint_ClearIN();
	}
}

// Prepare the next report for the host.
void GetNextReport(USB_JoystickReport_Input_t *const ReportData)
{
	// partially update the command.
	// used command will switch to a new if a new command has been completely set.
	updateCommands();

	// copy command to use
	memcpy(ReportData, &COMMAND_USED, sizeof(USB_JoystickReport_Input_t));
}

/** ISR to manage the reception of data from the serial port, placing received bytes into a circular buffer
 *  for later transmission to the host.
 */
ISR(USART1_RX_vect)
{
	uint8_t ReceivedByte = UDR1;
	RingBuffer_Insert(&RX_Buffer, ReceivedByte);
}
