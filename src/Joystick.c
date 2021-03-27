#include "Joystick.h"
#include "Bot.h"
#include <LUFA/Drivers/Peripheral/Serial.h>

typedef enum {
    SYNC_CONTROLLER,
    BREATHE,
    PROCESS,
    DONE
} State_t;

const __flash command STARTUP[] = {
    // Setup controller
                          { NOTHING,  250 },
    { TRIGGERS,   5 },    { NOTHING,  150 },
    { TRIGGERS,   5 },    { NOTHING,  150 },
    { A,          5 },    { NOTHING,  250 },

    // Go into game
    { HOME,       5 },    { NOTHING,  250 },
    { A,          5 },    { NOTHING,  250 },
};
const int STARTUP_LENGTH = sizeof(STARTUP) / sizeof(command);

void AS_Serial_SendString(char* s) {
    for (int i = 0; i < strlen(s); i += 1) {
        Serial_SendByte(s[i]);
    }
}

// Configures hardware and peripherals, such as the USB peripherals.
void SetupHardware(void) {
    // We need to disable watchdog if enabled by bootloader/fuses.
    MCUSR &= ~(1 << WDRF);
    wdt_disable();

    // We need to disable clock division before initializing the USB hardware.
    clock_prescale_set(clock_div_1);
    // We can then initialize our hardware and peripherals, including the USB stack.

    #ifdef ALERT_WHEN_DONE
    // Both PORTD and PORTB will be used for the optional LED flashing and buzzer.
    #warning LED and Buzzer functionality enabled. All pins on both PORTB and PORTD will toggle when printing is done.
    DDRD  = 0xFF; //Teensy uses PORTD
    PORTD =  0x0;
  //We'll just flash all pins on both ports since the UNO R3
    DDRB  = 0xFF; //uses PORTB. Micro can use either or, but both give us 2 LEDs
    PORTB =  0x0; //The ATmega328P on the UNO will be resetting, so unplug it?
    #endif
    // The USB stack should be initialized last.
    Serial_Init(9600, 0);
    AS_Serial_SendString("hello hello world\n");
    USB_Init();
}

// Fired to indicate that the device is enumerating.
void EVENT_USB_Device_Connect(void) {
    // We can indicate that we're enumerating here (via status LEDs, sound, etc.).
}

// Fired to indicate that the device is no longer connected to a host.
void EVENT_USB_Device_Disconnect(void) {
    // We can indicate that our device is not ready (via status LEDs, sound, etc.).
}

// Fired when the host set the current configuration of the USB device after enumeration.
void EVENT_USB_Device_ConfigurationChanged(void) {
    bool ConfigSuccess = true;

    // We setup the HID report endpoints.
    ConfigSuccess &= Endpoint_ConfigureEndpoint(JOYSTICK_OUT_EPADDR, EP_TYPE_INTERRUPT, JOYSTICK_EPSIZE, 1);
    ConfigSuccess &= Endpoint_ConfigureEndpoint(JOYSTICK_IN_EPADDR, EP_TYPE_INTERRUPT, JOYSTICK_EPSIZE, 1);

    // We can read ConfigSuccess to indicate a success or failure at this point.
}

// Process control requests sent to the device from the USB host.
void EVENT_USB_Device_ControlRequest(void) {
    // We can handle two control requests: a GetReport and a SetReport.

    // Not used here, it looks like we don't receive control request from the Switch.
}

void _empty_report(USB_JoystickReport_Input_t* report) {
    memset(report, 0, sizeof(USB_JoystickReport_Input_t));
    report->LX = STICK_CENTER;
    report->LY = STICK_CENTER;
    report->RX = STICK_CENTER;
    report->RY = STICK_CENTER;
    report->HAT = HAT_CENTER;
}

void GetNextReport_startup(
    USB_JoystickReport_Input_t* report,
    State_t* state,
    int* index,
    int* duration
) {
    _empty_report(report);

    switch (*state) {
        case SYNC_CONTROLLER:
            *state = BREATHE;
            break;

        case BREATHE:
            *state = PROCESS;
            break;

        case PROCESS:
            switch (STARTUP[*index].button) {
                case A:
                    report->Button |= SWITCH_A;
                    break;
                case HOME:
                    report->Button |= SWITCH_HOME;
                    break;
                case TRIGGERS:
                    report->Button |= SWITCH_L | SWITCH_R;
                    break;
                default:
                    report->LX = STICK_CENTER;
                    report->LY = STICK_CENTER;
                    report->RX = STICK_CENTER;
                    report->RY = STICK_CENTER;
                    report->HAT = HAT_CENTER;
                    break;
            }

            *duration += 1;

            if (*duration > STARTUP[*index].duration) {
                *index += 1;
                *duration = 0;
            }

            if (*index >= STARTUP_LENGTH) {
                *state = DONE;

                report->LX = STICK_CENTER;
                report->LY = STICK_CENTER;
                report->RX = STICK_CENTER;
                report->RY = STICK_CENTER;
                report->HAT = HAT_CENTER;

                return;
            }

            break;

        case DONE:
            break;
    }
}

void HID_Task_startup(State_t* state, int* index, int* duration) {
    if (USB_DeviceState != DEVICE_STATE_Configured)
        return;

    Endpoint_SelectEndpoint(JOYSTICK_OUT_EPADDR);
    if (Endpoint_IsOUTReceived()) {
        if (Endpoint_IsReadWriteAllowed()) {
            USB_JoystickReport_Output_t JoystickOutputData;
            while(Endpoint_Read_Stream_LE(&JoystickOutputData, sizeof(JoystickOutputData), NULL) != ENDPOINT_RWSTREAM_NoError);
        }
        Endpoint_ClearOUT();
    }

    Endpoint_SelectEndpoint(JOYSTICK_IN_EPADDR);
    if (Endpoint_IsINReady()) {
        USB_JoystickReport_Input_t JoystickInputData;
        GetNextReport_startup(&JoystickInputData, state, index, duration);
        while(Endpoint_Write_Stream_LE(&JoystickInputData, sizeof(JoystickInputData), NULL) != ENDPOINT_RWSTREAM_NoError);
        Endpoint_ClearIN();
    }
}

void GetNextReport(USB_JoystickReport_Input_t* report, uint8_t c) {
    _empty_report(report);

    switch (c) {
        case '0':
            break;

        case 'A':
            report->Button |= SWITCH_A;
            break;

        case 'B':
            report->Button |= SWITCH_B;
            break;

        case 'X':
            report->Button |= SWITCH_X;
            break;

        case 'Y':
            report->Button |= SWITCH_Y;
            break;

        case 'H':
            report->Button |= SWITCH_HOME;
            break;

        case '+':
            report->Button |= SWITCH_PLUS;
            break;

        case '-':
            report->Button |= SWITCH_MINUS;
            break;

        case 'L':
            report->Button |= SWITCH_L;
            break;

        case 'R':
            report->Button |= SWITCH_R;
            break;

        case 'w':
            report->LY = STICK_MIN;
            break;

        case 'a':
            report->LX = STICK_MIN;
            break;

        case 's':
            report->LY = STICK_MAX;
            break;

        case 'd':
            report->LX = STICK_MAX;
            break;

        case 'q':
            report->LY = STICK_MIN;
            report->LX = STICK_MIN;
            break;

        case 'e':
            report->LY = STICK_MIN;
            report->LX = STICK_MAX;
            break;

        case 'z':
            report->LY = STICK_MAX;
            report->LX = STICK_MIN;
            break;

        case 'c':
            report->LY = STICK_MAX;
            report->LX = STICK_MAX;
            break;
    }
}

void HID_Task(uint8_t c) {
    if (USB_DeviceState != DEVICE_STATE_Configured)
        return;

    Endpoint_SelectEndpoint(JOYSTICK_OUT_EPADDR);
    if (Endpoint_IsOUTReceived()) {
        if (Endpoint_IsReadWriteAllowed()) {
            USB_JoystickReport_Output_t JoystickOutputData;
            while(Endpoint_Read_Stream_LE(&JoystickOutputData, sizeof(JoystickOutputData), NULL) != ENDPOINT_RWSTREAM_NoError);
        }
        Endpoint_ClearOUT();
    }

    Endpoint_SelectEndpoint(JOYSTICK_IN_EPADDR);
    if (Endpoint_IsINReady()) {
        USB_JoystickReport_Input_t JoystickInputData;
        GetNextReport(&JoystickInputData, c);
        while(Endpoint_Write_Stream_LE(&JoystickInputData, sizeof(JoystickInputData), NULL) != ENDPOINT_RWSTREAM_NoError);
        Endpoint_ClearIN();
    }
}

int main(void) {
    SetupHardware();
    GlobalInterruptEnable();

    // perform startup task first (to enter the game)
    State_t state = SYNC_CONTROLLER;
    int index = 0;
    int duration = 0;
    while (state != DONE) {
        HID_Task_startup(&state, &index, &duration);
        USB_USBTask();
    }

    // listen for inputs and react
    char c = '0';
    for (;;) {
        if (Serial_IsCharReceived()) {
            c = Serial_ReceiveByte();
            AS_Serial_SendString("recv: ");
            Serial_SendByte(c);
            Serial_SendByte('\n');
        }

        HID_Task(c);
        USB_USBTask();
    }
}
