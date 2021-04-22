import re

from src.tutor.lessons.lesson import Lesson
from src.util import cw_meta


class Lesson4(Lesson):
	def __init__(self):
		super().__init__()
		self.number = 4
		self.lesson_title = f"E and T"
		self.lesson_description = f"A 'dash' is generally around 3x as long as a 'dot.' Maintain a steady pace. A \"█\"" \
			f" will represent an invalid character."

		self.target_text = 'T T TT E E EE ET TE ET TE ETET TETE ETET TETE'

	def key_event(self, cw_text):
		cw_text = re.sub("[^(TE )]", '█', cw_text)
		return cw_text
