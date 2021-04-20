import unittest

from src.cw.SymbolTracker import SymbolTracker


class TestSymbolTracker(unittest.TestCase):
	symbol_tracker = None

	def setUp(self):
		self.symbol_tracker = SymbolTracker()

	def test_default_wpm(self):
		self.assertEqual(self.symbol_tracker.wpm(), 5)
