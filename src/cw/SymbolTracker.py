import collections

from src.util import cw_meta


class SymbolTracker:
	DOWN = 'DOWN'
	UP = 'UP'

	def __init__(self):
		self._last_key_dir = self.UP
		self._last_key_time = 0
		self._symbol_rate = cw_meta.starting_rate
		self._symbol_queue = collections.deque(25*[(cw_meta.DIT, cw_meta.starting_rate)], 25)
		pass

	def keyed_down(self, time_ms):
		return self._key_event(self.UP, time_ms)

	def keyed_up(self, time_ms):
		return self._key_event(self.DOWN, time_ms)

	def _key_event(self, direction, time_ms):
		delta_time = time_ms - self._last_key_time
		self._last_key_time = time_ms
		self._last_key_dir = direction

		symbol = self.calculate_symbol(direction, delta_time, self.wpm())

		if self.is_long_wait(delta_time):
			symbol = cw_meta.NONE

		if symbol != cw_meta.NONE:
			self._symbol_queue.appendleft((symbol, delta_time))
		return symbol

	def calculate_symbol(self, direction, delta_time, wpm):
		dit_length = cw_meta.dit_ms(wpm)
		possible_dits = delta_time / dit_length

		result = None
		if direction == self.UP:
			next_word_timing = (cw_meta.cw_timing[cw_meta.NEXT_LETTER] + cw_meta.cw_timing[cw_meta.NEXT_WORD]) / 2
			if possible_dits < cw_meta.cw_timing[cw_meta.NEXT_LETTER]:
				result = None
			elif possible_dits < next_word_timing:
				result = cw_meta.NEXT_LETTER
			else:
				result = cw_meta.NEXT_WORD

		if direction == self.DOWN:
			rounded = int(possible_dits)
			if rounded <= cw_meta.cw_timing[cw_meta.DIT]:
				result = cw_meta.DIT
			else:
				result = cw_meta.DAH

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

