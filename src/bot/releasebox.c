#include "Bot.h"

const int ECHOES = 0;

const command INPUTS[] = {
	// Setup controller
						{ NOTHING,  250 },
	{ TRIGGERS,   5 },	{ NOTHING,  150 },
	{ TRIGGERS,   5 },	{ NOTHING,  150 },
	{ A,          5 },	{ NOTHING,  250 },

	// Go into game
	{ HOME,       5 },	{ NOTHING,  100 },
	{ HOME,       5 },	{ NOTHING,  100 },

	// 1a

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 1b
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 1c
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 1d
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 1e
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 1f
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 2f
	{ DOWN,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 2e
	{ LEFT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 2d
	{ LEFT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 2c
	{ LEFT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 2b
	{ LEFT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 2a
	{ LEFT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 3a
	{ DOWN,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 3b
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 3c
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 3d
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 3e
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 3f
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 4f
	{ DOWN,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 4e
	{ LEFT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 4d
	{ LEFT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 4c
	{ LEFT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 4b
	{ LEFT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 4a
	{ LEFT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 5a
	{ DOWN,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 5b
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 5c
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 5d
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 5e
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// go to 5f
	{ RIGHT,       5 },	{ NOTHING,  100 },

	// Release current position
	{ A,          5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  150 },
	{ UP,         5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  350 },
	{ A,          5 },	{ NOTHING,  100 },

	// finished - do nothing
};

const int INPUT_REPEAT_BEGIN = 488;
const int INPUTS_LENGTH = sizeof(INPUTS)/sizeof(command);
