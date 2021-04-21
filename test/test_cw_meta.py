from src.util import cw_meta
from test.base_test_setup import BaseTestSetup


class TestCwMeta(BaseTestSetup):
	def test_dit_rate_formula(self):
		wpm = cw_meta.wpm(1200)
		self.assertEqual(1, wpm)

	def test_wpm_rate_formula(self):
		dit = cw_meta.dit_ms(1)
		self.assertEqual(1200, dit)
