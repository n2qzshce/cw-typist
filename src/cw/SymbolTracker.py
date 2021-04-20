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
		self._key_event(self.UP, time_ms)
		pass

	def keyed_up(self, time_ms):
		self._key_event(self.DOWN, time_ms)
		pass

	def _key_event(self, direction, time_ms):
		if direction == self._last_key_dir:
			return

		self._last_key_time = time_ms
		self._last_key_dir = direction

	def wpm(self):
		sum = 0
		for x in self._symbol_queue:
			sum += x[1]

		average = sum / len(self._symbol_queue)
		wpm = cw_meta.wpm(average)
		return wpm
