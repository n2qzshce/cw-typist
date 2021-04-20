import time

starting_rate = 240  # milliseconds

DIT = 'DIT'
DAH = 'DAH'
NEXT_LETTER = 'NEXT_LETTER'
NEXT_WORD = 'NEXT_WORD'

cw_timing = {
	DIT: 1,
	DAH: 3,
	NEXT_LETTER: 3,
	NEXT_WORD: 7,
}


def wpm(dit_length_ms):
	return 60 / (50 * dit_length_ms / 1000)


def tick_ms():
	nanos = time.monotonic_ns()
	millis = nanos / 1000000
	return millis
