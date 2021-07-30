from src.util import cw_meta
from src.util.listen_lesson import ListenLesson


class Listen5IandM(ListenLesson):
	def __init__(self):
		super().__init__()
		self.lesson_title = f"I: {cw_meta.formatted('I')} M: {cw_meta.formatted('M')}"
		self.lesson_description = f"Morse letters are made of a combination of long and short pulses. Any given" \
			f"letter will usually be a series of pulses."

		self.target_text = 'IIMMIIMMIIMM II MM II MM IMIM MIMI I M IM M I MI'

