#include "Bot.h"

const int ECHOES = 0;

const __flash command INPUTS[] = {
	// Setup controller
						{ NOTHING,  250 },
	{ TRIGGERS,   5 },	{ NOTHING,  150 },
	{ TRIGGERS,   5 },	{ NOTHING,  150 },
	{ A,          5 },	{ NOTHING,  250 },

	// Go into game
	{ HOME,       5 },	{ NOTHING,  100 },
	{ HOME,       5 },	{ NOTHING,  150 },

	// Energie strömt aus dem Pokemon-Nest!
	{ A,          5 },	{ NOTHING,  350 },
	// (Du erhälst 2 000 Watt!)
	{ B,          5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  100 },
	{ B,          5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  100 },
	{ B,          5 },	{ NOTHING,  200 },

	// Reopen dialog (this helps with the month reset)
	{ A,       5 },			{ NOTHING,  100 },

	// Mitspieler suchen
	{ A,       5 },			{ NOTHING,  800 },
	// One day forward
	{ HOME,       5 },		{ NOTHING,  100 },
	{ DOWN,       5 },		{ NOTHING,  100 },
	{ RIGHT,      5 },		{ NOTHING,  50 },
	{ RIGHT,      5 },		{ NOTHING,  50 },
	{ RIGHT,      5 },		{ NOTHING,  50 },
	{ RIGHT,      5 },		{ NOTHING,  50 },
	{ A,					5 },		{ NOTHING,	100 },
	// scroll to console
	{ DOWN,       180 },	{ NOTHING,	50 },
	{ A,          5 },		{ NOTHING,  50 },

	// go to date and time
	{ DOWN,       5 },		{ NOTHING,  50 },
	{ DOWN,       5 },		{ NOTHING,  50 },
	{ DOWN,       5 },		{ NOTHING,  50 },
	{ DOWN,       5 },		{ NOTHING,  50 },
	{ A,          5 },		{ NOTHING,  50 },

	// go to date and time setting
	{ DOWN,       5 },		{ NOTHING,  50 },
	{ DOWN,       5 },		{ NOTHING,  50 },
	{ DOWN,       5 },		{ NOTHING,  50 },
	{ A,          5 },		{ NOTHING,  100 },

	// set one day forward
	{ UP,         5 },		{ NOTHING,  50 },
	{ RIGHT,      90 },		{ NOTHING,  50 },
	{ A,          5 },		{ NOTHING,  50 },

	// Go back into game
	{ HOME,       5 },		{ NOTHING,  100 },
	{ HOME,       5 },		{ NOTHING,  100 },

	// Willst du die Suche nach Mitspielern abbrechen?
	{ B,          5 },		{ NOTHING,  150 },

	// Ja
	{ A,          5 },		{ NOTHING,  200 },
};

const int INPUT_REPEAT_BEGIN = 11;
const int INPUTS_LENGTH = sizeof(INPUTS)/sizeof(command);
