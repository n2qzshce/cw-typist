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
		symbol = self.symbol_tracker.calculate_symbol(SymbolTracker.DOWN, 1200, 1)
		self.assertEqual(cw_meta.DIT, symbol)

	def test_dah(self):
		symbol = self.symbol_tracker.calculate_symbol(SymbolTracker.DOWN, 1200 * 7, 1)
		self.assertEqual(cw_meta.DAH, symbol)

	def test_next_char(self):
		symbol = self.symbol_tracker.calculate_symbol(SymbolTracker.UP, 1200 * 3, 1)
		self.assertEqual(cw_meta.NEXT_LETTER, symbol)

	def test_next_word(self):
		symbol = self.symbol_tracker.calculate_symbol(SymbolTracker.UP, 1200 * 7, 1)
		self.assertEqual(cw_meta.NEXT_WORD, symbol)

	def test_long_wait(self):
		first_wait = self.symbol_tracker.is_long_wait(1200 * 7)
		second_wait = self.symbol_tracker.is_long_wait(60000)
		self.assertFalse(first_wait)
		self.assertTrue(second_wait)
