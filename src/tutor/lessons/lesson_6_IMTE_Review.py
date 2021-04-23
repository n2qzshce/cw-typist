import re

from src.util import cw_meta
from src.util.lesson import Lesson


class Lesson6IMTEReview(Lesson):
	def __init__(self):
		super().__init__()
		self.lesson_title = f"Reviewing I, M, T, and E"
		self.lesson_description = f"This is a longer exercise to help you practice I, M, T, and E"

		self.target_text = 'EEEE TTTT IIII MMMM ETETETET IMIMIMIM EIEIEIEI TMTMTMTM EMEMEMEMEM TITITITITI' \
			' I ME TIM TIME ME I EMIT I TIME EM MITE TIE'

	def key_event(self, cw_text):
		cw_text = re.sub("[^(IMTE )]", '█', cw_text)
		return cw_text
