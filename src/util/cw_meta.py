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
	NEXT_LETTER: '',
	NEXT_WORD: ' ',
}


def wpm(dit_length_ms):
	return 60 / (50 * dit_length_ms / 1000)


def dit_ms(words_per_minute):
	return 60 / (50 * words_per_minute) * 1000


def tick_ms():
	nanos = time.monotonic_ns()
	millis = nanos / 1000000
	return millis