import unittest
from src.util import cw_meta


class TestCwMeta(unittest.TestCase):
	def test_dit_rate_formula(self):
		wpm = cw_meta.wpm(1200)
		self.assertEqual(1, wpm)
