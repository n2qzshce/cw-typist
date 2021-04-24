import collections

from src.cw.SymbolTracker import SymbolTracker
from src.util import cw_meta
from test.base_test_setup import BaseTestSetup


class TestSymbolTracker(BaseTestSetup):
	symbol_tracker = None
	base_wpm = 5
	base_dits = 200

	def setUp(self):
		self.symbol_tracker = SymbolTracker()

	def test_default_wpm(self):
		self.assertEqual(self.symbol_tracker.wpm(), 6)

	def test_dit(self):
		symbol = self.symbol_tracker.calculate_symbol(self.base_dits, 1)
		self.assertEqual(cw_meta.DIT, symbol)

	def test_dah(self):
		symbol = self.symbol_tracker.calculate_symbol(self.base_dits * 7, 1)
		self.assertEqual(cw_meta.DAH, symbol)

	def test_long_wait(self):
		first_wait = self.symbol_tracker.is_long_wait(self.base_dits * 7)
		second_wait = self.symbol_tracker.is_long_wait(60000)
		self.assertFalse(first_wait)
		self.assertTrue(second_wait)

	def test_gets_e(self):
		self.symbol_tracker.keyed_up(240)
		self.symbol_tracker.keyed_down(self.symbol_tracker._last_key_time + 240 * 3)
		symbol = self.symbol_tracker.next_letter()
		self.assertEqual('E', symbol)

	def test_gets_n(self):
		self.symbol_tracker.keyed_up(240 * 3)
		self.symbol_tracker.keyed_down(self.symbol_tracker._last_key_time + 1)
		self.symbol_tracker.keyed_up(self.symbol_tracker._last_key_time + 240)
		self.symbol_tracker.keyed_down(self.symbol_tracker._last_key_time + 240 * 3)
		symbol = self.symbol_tracker.next_letter()
		self.assertEqual('N', symbol)

	def test_next_letter_timing(self):
		timing = self.symbol_tracker.next_letter_timing()
		self.assertEqual(self.base_dits * 2 / 1000, timing)

	def test_next_word_timing(self):
		timing = self.symbol_tracker.next_word_timing()
		self.assertEqual(self.base_dits * 5 / 1000, timing)

	def test_next_letter_clears_buffer(self):
		self.symbol_tracker._letter_built = collections.deque([cw_meta.DIT]*7, 7)
		symbol = self.symbol_tracker.next_letter()
		after = list(self.symbol_tracker._letter_built)
		self.assertEqual([], after)
