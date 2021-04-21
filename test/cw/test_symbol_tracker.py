from src.cw.SymbolTracker import SymbolTracker
from src.util import cw_meta
from test.base_test_setup import BaseTestSetup


class TestSymbolTracker(BaseTestSetup):
	symbol_tracker = None
	base_wpm = 5
	base_dits = 1200

	def setUp(self):
		self.symbol_tracker = SymbolTracker()

	def test_default_wpm(self):
		self.assertEqual(self.symbol_tracker.wpm(), 5)

	def test_dit(self):
		symbol = self.symbol_tracker.calculate_symbol(SymbolTracker.DOWN_TO_UP, 1200, 1)
		self.assertEqual(cw_meta.DIT, symbol)

	def test_dah(self):
		symbol = self.symbol_tracker.calculate_symbol(SymbolTracker.DOWN_TO_UP, 1200 * 7, 1)
		self.assertEqual(cw_meta.DAH, symbol)

	def test_next_char(self):
		symbol = self.symbol_tracker.calculate_symbol(SymbolTracker.UP_TO_DOWN, 1200 * 3, 1)
		self.assertEqual(cw_meta.NEXT_LETTER, symbol)

	def test_next_word(self):
		symbol = self.symbol_tracker.calculate_symbol(SymbolTracker.UP_TO_DOWN, 1200 * 7, 1)
		self.assertEqual(cw_meta.NEXT_WORD, symbol)

	def test_long_wait(self):
		first_wait = self.symbol_tracker.is_long_wait(1200 * 7)
		second_wait = self.symbol_tracker.is_long_wait(60000)
		self.assertFalse(first_wait)
		self.assertTrue(second_wait)

	def test_gets_e(self):
		self.symbol_tracker._last_key_dir = SymbolTracker.UP_TO_DOWN
		symbol = self.symbol_tracker.keyed_up(240)
		symbol = self.symbol_tracker.keyed_down(self.symbol_tracker._last_key_time + 240 * 3)
		self.assertEqual('E', symbol)

	def test_gets_n(self):
		self.symbol_tracker._last_key_dir = SymbolTracker.UP_TO_DOWN
		symbol = self.symbol_tracker.keyed_up(240 * 3)
		symbol = self.symbol_tracker.keyed_down(self.symbol_tracker._last_key_time + 1)
		symbol = self.symbol_tracker.keyed_up(self.symbol_tracker._last_key_time + 240)
		symbol = self.symbol_tracker.keyed_down(self.symbol_tracker._last_key_time + 240 * 3)
		self.assertEqual('N', symbol)
