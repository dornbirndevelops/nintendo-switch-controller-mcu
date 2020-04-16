#ifndef _BOT_H_
#define _BOT_H_

#include <stdint.h>

typedef enum {
	UP,
	DOWN,
	LEFT,
	RIGHT,
	SPIN,
	POSITION,
	X,
	Y,
	A,
	B,
	L,
	R,
	PLUS,
	MINUS,
	HOME,
	NOTHING,
	TRIGGERS
} Buttons_t;

typedef struct {
	Buttons_t button;
	uint16_t duration;
} command;

extern const __flash command INPUTS[];
extern const int INPUTS_LENGTH;
extern const int INPUT_REPEAT_BEGIN;
extern const int ECHOES;

#endif
