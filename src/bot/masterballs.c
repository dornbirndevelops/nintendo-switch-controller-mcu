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

	// Sei gegruesst! Womit kann ich dir helfen?
	{ A,          5 },	{ NOTHING,  250 },
	// Auswahl Menü
	{ A,          5 },	{ NOTHING,  100 },
	// Zu ID-Lotterie
	{ DOWN,       5 },	{ NOTHING,  100 },
	// Bestätige Auswahl
	{ A,          5 },	{ NOTHING,  250 },
	// Einen Moment, bitte... Verbindung zzzum ID-Lotterie-Zzzentrum hergestellt!
	{ A,          5 },	{ NOTHING,  250 },
	// Wenn die gezzzogene Losnummer der ID eines deiner Pokemon entspricht, hast du die
	{ A,          5 },	{ NOTHING,  250 },
	// Möglichkeit, großartige Preise zzzu gewinnen!
	{ A,          5 },	{ NOTHING,  500 },
	// Möchtest du dein Glück versuchen? Dann musst du jetzzzt speichern, um ein Los zzzu zzziehen.
	{ A,          5 },	{ NOTHING,  500 },
	// Du hast das Spiel gespeichert.
	{ A,          5 },	{ NOTHING,  100 },
	// Alles klar! Viel Glück bei der Zzziehung!
	{ A,          5 },	{ NOTHING,  100 },
	// ... ... ...
	{ A,          5 },	{ NOTHING,  100 },
	// Das Los hat die Nummer xxxxx!
	{ A,          5 },	{ NOTHING,  250 },
	// Dann wollen wir jetzzzt mal sehen, ob sie mit der ID eines deiner Pokemon übereinstimmt...
	{ A,          5 },	{ NOTHING,  500 },
	// sound
	// Herzlichen Glückwunsch!
	{ A,          5 },	{ NOTHING,  250 },
	// Die ID von Name, einem Pokemon in deinen PC-Boxen, enthält mindestens eine
	{ A,          5 },	{ NOTHING,  150 },
	// Übereinstimmung mit der Losnummer!
	{ B,          5 },	{ NOTHING,  100 },
	// 1-5 Ziffern stimmen überein!
	{ B,          5 },	{ NOTHING,  100 },
	// So viel Glück muss man erst mal haben! Du hast damit den xxxten Preis gewonnen:
	{ B,          5 },	{ NOTHING,  100 },
	// ein Item ...!
	{ B,          5 },	{ NOTHING,  100 },
	// Du erhälst Item!
	{ B,          5 },	{ NOTHING,  100 },
	// Du verstaust Item in der ...tasche.
	{ B,          5 },	{ NOTHING,  100 },
	// Ich freue mich schon auf die nächste Zzziehung!
	{ B,          5 },	{ NOTHING,  100 },
	{ B,          5 },	{ NOTHING,  100 },
	{ B,          5 },	{ NOTHING,  100 },
	{ B,          5 },	{ NOTHING,  100 },

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

	{ HOME,       5 },		{ NOTHING,  100 },
	{ HOME,       5 },		{ NOTHING,  100 },
};

const int INPUT_REPEAT_BEGIN = 11;
const int INPUTS_LENGTH = sizeof(INPUTS)/sizeof(command);
