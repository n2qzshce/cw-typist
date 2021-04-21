import time

starting_rate = 240  # milliseconds

NONE = None
DIT = 'DIT'
DAH = 'DAH'
NEXT_LETTER = 'NEXT_LETTER'
NEXT_WORD = 'NEXT_WORD'

cw_timing = {
	NONE: 1,
	DIT: 1,
	DAH: 3,
	NEXT_LETTER: 3,
	NEXT_WORD: 7,
}

cw_printed = {
	NONE: None,
	DIT: '.',
	DAH: '_',
	NEXT_LETTER: '^',
	NEXT_WORD: ' ',
}

cw_dict = {
	'A': [DIT, DAH],
	'B': [DAH, DIT, DIT, DIT],
	'C': [DAH, DIT, DAH, DIT],
	'D': [DAH, DIT, DIT],
	'E': [DIT],
	'F': [DIT, DIT, DAH, DIT],
	'G': [DAH, DAH, DIT],
	'H': [DIT, DIT, DIT, DIT],
	'I': [DIT, DIT],
	'J': [DIT, DAH, DAH, DAH],
	'K': [DAH, DIT, DAH],
	'L': [DIT, DAH, DIT, DIT],
	'M': [DAH, DAH],
	'N': [DAH, DIT],
	'O': [DAH, DAH, DAH],
	'P': [DIT, DAH, DAH, DIT],
	'Q': [DAH, DAH, DIT, DAH],
	'R': [DIT, DAH, DIT],
	'S': [DIT, DIT, DIT],
	'T': [DAH],
	'U': [DIT, DIT, DAH],
	'V': [DIT, DIT, DIT, DAH],
	'W': [DIT, DAH, DAH],
	'X': [DAH, DIT, DIT, DAH],
	'Y': [DAH, DIT, DAH, DAH],
	'Z': [DAH, DAH, DIT, DIT],
	'1': [DIT, DAH, DAH, DAH, DAH],
	'2': [DIT, DIT, DAH, DAH, DAH],
	'3': [DIT, DIT, DIT, DAH, DAH],
	'4': [DIT, DIT, DIT, DIT, DAH],
	'5': [DIT, DIT, DIT, DIT, DIT],
	'6': [DAH, DIT, DIT, DIT, DIT],
	'7': [DAH, DAH, DIT, DIT, DIT],
	'8': [DAH, DAH, DAH, DIT, DIT],
	'9': [DAH, DAH, DAH, DAH, DIT],
	'0': [DAH, DAH, DAH, DAH, DAH],
	'.': [DIT, DAH, DIT, DAH, DIT, DAH],
	',': [DAH, DAH, DIT, DIT, DAH, DAH],
	'?': [DIT, DIT, DAH, DAH, DIT, DIT],
	'/': [DAH, DIT, DIT, DAH, DIT],
}
no_chr_found = '█'


def find_letter(sequence):
	result = no_chr_found
	listed_seq = list(sequence)
	listed_seq.reverse()

	for x in listed_seq:
		if x == NEXT_LETTER or x == NEXT_WORD:
			listed_seq.remove(x)

	for character in cw_dict:
		if cw_dict[character] == listed_seq:
			result = character
			break
	return result


def wpm(dit_length_ms):
	return 60 / (50 * dit_length_ms / 1000)


def dit_ms(words_per_minute):
	return 60 / (50 * words_per_minute) * 1000


def tick_ms():
	nanos = time.monotonic_ns()
	millis = nanos / 1000000
	return millis

