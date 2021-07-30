import collections

from src.util import cw_meta
from test.base_test_setup import BaseTestSetup


class TestCwMeta(BaseTestSetup):
	def test_dit_rate_formula(self):
		wpm = cw_meta.wpm(1200)
		self.assertEqual(1, wpm)

	def test_wpm_rate_formula(self):
		dit = cw_meta.symbol_ms(1, cw_meta.DIT)
		self.assertEqual(1200, dit)

	def test_letter_e(self):
		seq = collections.deque([cw_meta.DIT], 7)
		letter = cw_meta.find_letter(seq)
		self.assertEqual('E', letter)

	def test_letter_t(self):
		seq = collections.deque([cw_meta.DAH], 7)
		letter = cw_meta.find_letter(seq)
		self.assertEqual('T', letter)

	def test_no_chr_found(self):
		seq = collections.deque(6*[cw_meta.DIT], 7)
		letter = cw_meta.find_letter(seq)
		self.assertEqual(cw_meta.no_chr_found, letter)

	def test_character_formatting(self):
		result = cw_meta.formatted('?')
		self.assertEqual('••——••', result)

	def test_builds_message(self):
		result = cw_meta.build_sequence('EE')
		self.assertEqual([cw_meta.DIT, cw_meta.NEXT_LETTER, cw_meta.DIT], result)

	def test_builds_multiple_words(self):
		result = cw_meta.build_sequence('T E')
		self.assertEqual([cw_meta.DAH, cw_meta.NEXT_WORD, cw_meta.DIT], result)
