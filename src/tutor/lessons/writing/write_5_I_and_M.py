import re

from src.util import cw_meta
from src.util.write_lesson import WriteLesson


class Write5IandM(WriteLesson):
	def __init__(self):
		super().__init__()
		self.lesson_title = f"I: {cw_meta.formatted('I')} M: {cw_meta.formatted('M')}"
		self.lesson_description = f"Morse letters are made of a combination of long and short pulses. Use a short pause" \
			f" to indicate the end of a letter, and a long pause to indicate the end of a word."

		self.target_text = 'IIMMIIMMIIMM II MM II MM IMIM MIMI I M IM M I MI'

	def key_event(self, cw_text):
		cw_text = re.sub("[^(IMTE )]", '█', cw_text)
		return cw_text
