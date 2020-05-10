#include <stdint.h>
#include <stdbool.h>

#include <avr/io.h>
#include <avr/interrupt.h>

#include <LUFA/Drivers/Peripheral/Serial.h>
#include <LUFA/Drivers/Board/LEDs.h>

#include "LightweightRingBuff.h"

RingBuff_t RX_Buffer;
RingBuff_t TX_Buffer;

// Configures hardware and peripherals, such as the USB peripherals.
void SetupHardware(void) {
    // serial init with interrupts
    Serial_Init(9600, false);
    UCSR1B |= (1<<RXCIE1);

    // LED init
    LEDs_Init();
}

void SetupSoftware(void) {
    RingBuffer_InitBuffer(&RX_Buffer);
    RingBuffer_InitBuffer(&TX_Buffer);
}

void Setup(void) {
    SetupSoftware();
    SetupHardware();
}

bool CanWrite(void) {
    return !RingBuffer_IsFull(&TX_Buffer);
}

void Write(const uint8_t data) {
    RingBuffer_Insert(&TX_Buffer, data);
    // activate interrupt for transmit register empty
    UCSR1B |= (1<<UDRIE1);
}

bool CanRead(void) {
    return !RingBuffer_IsEmpty(&RX_Buffer);
}

uint8_t Read(void) {
    return RingBuffer_Remove(&RX_Buffer);
}

void Loop(void) {
    static uint8_t state = 0;

    if (CanRead()) {
        state = Read();
        if (state) {
            LEDs_TurnOnLEDs(LEDMASK_RX);
        } else {
            LEDs_TurnOffLEDs(LEDMASK_RX);
        }
    }
}

// Main entry point.
int main(void) {
	Setup();

	GlobalInterruptEnable();

	for (;;)
		Loop();
}

ISR(USART1_UDRE_vect)
{
    if (!RingBuffer_IsEmpty(&TX_Buffer)) {
        UDR1 = RingBuffer_Remove(&TX_Buffer);
    } else {
        // deactivate isr when there is no data to send
        UCSR1B &= ~(1<<UDRIE1);
    }
}

ISR(USART1_RX_vect)
{
	volatile uint8_t ReceivedByte = UDR1;
	RingBuffer_Insert(&RX_Buffer, ReceivedByte);
}
