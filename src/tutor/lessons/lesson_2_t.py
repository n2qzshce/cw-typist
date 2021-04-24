import re

from src.util.lesson import Lesson
from src.util import cw_meta


class Lesson2T(Lesson):
	def __init__(self):
		super().__init__()
		self.lesson_title = f"T: {cw_meta.formatted('T')}"
		self.lesson_description = f"Where 'E' is represented with a short pulse ('dot'), 'T' is represented with a long " \
			f"pulse ('dash'). This pulse is generally 3x longer than your short pulse."

		self.target_text = 'TTTTEEEETTEE'

	def key_event(self, cw_text):
		cw_text = re.sub("[^TE]", '', cw_text)
		return cw_text


