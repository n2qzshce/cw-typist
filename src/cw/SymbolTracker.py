import collections
import logging

from src.util import cw_meta


class SymbolTracker:
	DOWN_TO_UP = 'DOWN_TO_UP'
	UP_TO_DOWN = 'UP_TO_DOWN'

	def __init__(self):
		self._last_key_time = 0
		self._symbol_rate = cw_meta.starting_rate
		self._symbol_queue = collections.deque(25*[(cw_meta.DIT, cw_meta.starting_rate)], 25)
		self._letter_built = collections.deque([], 7)
		pass

	def keyed_down(self, time_ms):
		self._last_key_time = time_ms

	def keyed_up(self, time_ms):
		delta_time = time_ms - self._last_key_time
		self._last_key_time = time_ms

		symbol = self.calculate_symbol(delta_time, self.wpm())

		if self.is_long_wait(delta_time):
			symbol = cw_meta.NONE

		if symbol != cw_meta.NONE:
			self._symbol_queue.appendleft((symbol, delta_time))
			self._letter_built.appendleft(symbol)

	def next_letter(self):
		letter = cw_meta.find_letter(self._letter_built)
		self._letter_built = collections.deque([], 7)
		return letter

	def next_letter_timing(self):
		wpm = self.wpm()
		dit_length = cw_meta.dit_ms(wpm)
		result = cw_meta.cw_timing[cw_meta.NEXT_LETTER] * dit_length / 1000
		return result

	def next_word_timing(self):
		wpm = self.wpm()
		dit_length = cw_meta.dit_ms(wpm)
		result = cw_meta.cw_timing[cw_meta.NEXT_WORD] * dit_length / 1000
		return result

	def calculate_symbol(self, delta_time, wpm):
		dit_length = cw_meta.dit_ms(wpm)
		possible_dits = delta_time / dit_length

		rounded = int(possible_dits)
		if rounded <= cw_meta.cw_timing[cw_meta.DIT]:
			result = cw_meta.DIT
		else:
			result = cw_meta.DAH

		logging.debug(f"CW Symbol: `{result}`")
		return result

	def wpm(self):
		dit_sum = 0
		for x in self._symbol_queue:
			symbol_time = x[1]
			score = cw_meta.cw_timing[x[0]]
			dit_sum += symbol_time / score

		average = dit_sum / len(self._symbol_queue)
		wpm = cw_meta.wpm(average)
		return wpm

	def is_long_wait(self, delta_time):
		space_time = cw_meta.starting_rate * cw_meta.cw_timing[cw_meta.NEXT_WORD]

		result = False
		long_interval = space_time * 10
		if delta_time > long_interval:
			result = True

		return result
