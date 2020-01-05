#include "Bot.h"

const int ECHOES = 2;

const command INPUTS[] = {
	// Setup controller
						{ NOTHING,  250 },
	{ TRIGGERS,   5 },	{ NOTHING,  150 },
	{ TRIGGERS,   5 },	{ NOTHING,  150 },
	{ A,          5 },	{ NOTHING,  250 },

	// Go into game
	{ HOME,       5 },	{ NOTHING,  250 },
	{ A,          5 },	{ NOTHING,  250 },

	// enter den with 2000 watts
	{ A,          5 },	{ NOTHING,  10 },
	{ A,          5 },	{ NOTHING,  10 },
	{ A,          5 },	{ NOTHING,  20 },

	// start search
	{ A,          5 },	{ NOTHING,  300 },

	// one day backward
	{ HOME,       5 },		{ NOTHING,  80 },
	{ DOWN,       5 },		{ NOTHING,  2 },
	{ RIGHT,      5 },		{ NOTHING,  1 },
	{ RIGHT,      5 },		{ NOTHING,  1 },
	{ RIGHT,      5 },		{ NOTHING,  1 },
	{ RIGHT,      5 },		{ NOTHING,  1 },
	{ A,          5 },		{ NOTHING,  40 },
	{ DOWN,       90 },		{ NOTHING,  10 },
	{ A,          5 },		{ NOTHING,  20 },
	{ DOWN,       5 },		{ NOTHING,  5 },
	{ DOWN,       5 },		{ NOTHING,  5 },
	{ DOWN,       5 },		{ NOTHING,  5 },
	{ DOWN,       5 },		{ NOTHING,  5 },
	{ A,          5 },		{ NOTHING,  20 },
	{ DOWN,       5 },		{ NOTHING,  5 },
	{ DOWN,       5 },		{ NOTHING,  5 },
	{ A,          5 },		{ NOTHING,  20 },
	{ DOWN,       5 },		{ NOTHING,  5 },
	{ RIGHT,      25 },		{ NOTHING,  5 },
	{ A,          5 },		{ NOTHING,  5 },
	{ HOME,       5 },		{ NOTHING,  80 },
	{ A,          5 },		{ NOTHING,  20 },

	// leave den
	{ B,          5 },		{ NOTHING,  40 },
	{ A,          5 },		{ NOTHING,  220 },

	// enter den without 2000 watts
	{ A,          5 },		{ NOTHING,  20 },

	// start search
	{ A,          5 },		{ NOTHING,  300 },

	// one day forward
	{ HOME,       5 },		{ NOTHING,  80 },
	{ DOWN,       5 },		{ NOTHING,  2 },
	{ RIGHT,      5 },		{ NOTHING,  1 },
	{ RIGHT,      5 },		{ NOTHING,  1 },
	{ RIGHT,      5 },		{ NOTHING,  1 },
	{ RIGHT,      5 },		{ NOTHING,  1 },
	{ A,          5 },		{ NOTHING,  40 },
	{ DOWN,       90 },		{ NOTHING,  10 },
	{ A,          5 },		{ NOTHING,  20 },
	{ DOWN,       5 },		{ NOTHING,  5 },
	{ DOWN,       5 },		{ NOTHING,  5 },
	{ DOWN,       5 },		{ NOTHING,  5 },
	{ DOWN,       5 },		{ NOTHING,  5 },
	{ A,          5 },		{ NOTHING,  20 },
	{ DOWN,       5 },		{ NOTHING,  5 },
	{ DOWN,       5 },		{ NOTHING,  5 },
	{ A,          5 },		{ NOTHING,  20 },
	{ UP,         5 },		{ NOTHING,  5 },
	{ RIGHT,      25 },		{ NOTHING,  5 },
	{ A,          5 },		{ NOTHING,  5 },
	{ HOME,       5 },		{ NOTHING,  80 },
	{ A,          5 },		{ NOTHING,  20 },

	// leave den
	{ B,          5 },		{ NOTHING,  40 },
	{ A,          5 },		{ NOTHING,  220 },

};

const int INPUT_REPEAT_BEGIN = 11;
const int INPUTS_LENGTH = sizeof(INPUTS)/sizeof(command);
