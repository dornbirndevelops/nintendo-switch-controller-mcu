#include "Bot.h"

/*

https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_Egg_cycles

 5 cycles =  700 !! DO NOT FORGET TO UNCOMMENT THE "if 5 cycles (Magikarp)" PARTS !!
10 cycles = 1400
15 cycles = 2100
20 cycles = 2800 (default)
25 cycles = 3500
30 cycles = 4200
35 cycles = 4900
40 cycles = 5600

*/
#define cycles 2800

const int ECHOES = 2;

const command INPUTS[] = {
	// Setup controller
						{ NOTHING,  150 },
	{ TRIGGERS,   5 },	{ NOTHING,  150 },
	{ TRIGGERS,   5 },	{ NOTHING,  150 },
	{ A,          5 },	{ NOTHING,  100 },

	// Open game
	{ HOME,       5 },	{ NOTHING,  100 },
	{ A,          5 },	{ NOTHING,  100 },

	/* ###### Pokemon slot 2 ###### */
	// teleport to daycare in wildarea
	{ X,          5 },	{ NOTHING,  100 }, //open menu
	{ A,          5 },	{ NOTHING,  100 }, 
	{ A,          5 },	{ NOTHING,  100 }, //you want to teleport here?
	{ A,          5 },	{ NOTHING,  100 }, //sure!

	// walk to daycare and get an egg
	{ DOWN,      70 },	{ NOTHING,    5 }, //walk down to daycare
	{ LEFT,       5 },	{ NOTHING,    5 }, //a little bit left
	{ A,          5 },	{ NOTHING,  100 }, //talk to her "I have an egg for you, do you want it?"
 	{ A,          5 },	{ NOTHING,  200 }, //yes I do
	{ A,          5 },	{ NOTHING,  100 }, //you got it
	{ A,          5 },	{ NOTHING,  100 }, //Put egg on your team
	{ A,          5 },	{ NOTHING,  100 }, //please select the slot!
	{ DOWN,       5 },	{ NOTHING,    5 }, //select correct pokemon slot
	{ A,          5 },	{ NOTHING,  100 }, //You sure want to put it here?
	{ A,          5 },	{ NOTHING,  200 }, //Yes!
	{ A,          5 },	{ NOTHING,  100 }, //take good care of it

	// start hatching
	{ PLUS,       5 },	{ NOTHING,    5 }, //get on your bike
	{ POSITION,  50 },	{ NOTHING,    5 },
	{ UP,        20 },	{ NOTHING,    5 },
	{ POSITION,  60 },	{ NOTHING,    5 }, //get into position
	{ SPIN,  cycles },	{ NOTHING,    5 }, //spin for X cycles

	// egg hatched?
	{ A,          5 },	{ NOTHING, 	825 }, //Oh
	{ A,          5 },	{ NOTHING, 	125 }, //"Pokemon" hatched from the egg
	{ B,          5 },	{ NOTHING, 	 10 },

	// if 5 cycles (Magikarp) 
	/*{ SPIN,  cycles },	{ NOTHING,    5 }, // extra rounds to make sure daycare have an egg
	{ A,          5 },	{ NOTHING, 	825 },
	{ A,          5 },	{ NOTHING, 	125 },
	{ B,          5 },	{ NOTHING, 	 10 },*/

	{ PLUS,       5 },	{ NOTHING,  100 }, //get off the bike

	// repeat
};

const int INPUT_REPEAT_BEGIN = 11;
const int INPUTS_LENGTH = sizeof(INPUTS)/sizeof(command);
