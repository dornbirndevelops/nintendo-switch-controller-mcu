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

	{ A,          5 },
	{ NOTHING,  220 }, // Hm? Du hast ja ein paar Fossilien. Würdest du sie mir mal zeigen?
	{ A,          5 },
	{ NOTHING,  220 }, // Also, mit welchem Fossil glaubst du, meine hohen Standards zu erfüllen?
	{ DOWN,       5 },
	{ NOTHING,  50 },
	{ A,       		5 },
	{ NOTHING,  200 }, // Und mit welchem Fossil willst du mein unstillbares Interesse wecken?
	{ A,          5 },
	{ NOTHING,  250 }, // Soll ich das Fischfossil zusammen mit dem Drachenfossil in ein Pokemon zurückverwandeln?
	{ A,          5 },
	{ NOTHING,  250 }, // Na schön! Sehen wir doch mal, ob wir das Rätsel dieser Fossilien lösen können!
	{ B,          5 },
	{ NOTHING,  600 }, // So, das hier hin... Und dann das dort hin... Ja... So ist's gut... Das sollte passen!
	{ B,          5 },
	{ NOTHING,  300 }, // Mission abgeschlossen! Offenbar war die Rückverwandlung ein voller Erfolg!
	{ B,          5 },
	{ NOTHING,  200 }, // Ich kann mir richtig gut vorstellen, wie dieses Pokemon in Urzeiten durch die Galar-Region
	{ B,          5 },
	{ NOTHING,  200 }, // gestreift ist! Pass gut auf es auf, ja?
	{ B,          5 },
	{ NOTHING,  800 }, // Pescragon erhalten!
	{ B,          5 },
	{ NOTHING,  400 }, // Pescragon wurde Team oder Box ...
	{ B,          5 },
	{ NOTHING,  200 }, // end dialog
};

const int INPUT_REPEAT_BEGIN = 11;
const int INPUTS_LENGTH = sizeof(INPUTS)/sizeof(command);
