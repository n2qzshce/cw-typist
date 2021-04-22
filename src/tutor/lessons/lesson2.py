import re

from src.tutor.lessons.lesson import Lesson
from src.util import cw_meta


class Lesson2(Lesson):
	def __init__(self):
		super().__init__()
		self.number = 2
		self.lesson_title = "Spacing:"
		self.lesson_description = f"To send a space, leave a pause in between your letters.\n" \
			f"Don't worry about missed symbols, just focus on the next symbol."

		self.target_text = 'EE E EEE E EE EEE'

	def key_event(self, cw_text):
		cw_text = re.sub("[^(E )]", '', cw_text)
		return cw_text
