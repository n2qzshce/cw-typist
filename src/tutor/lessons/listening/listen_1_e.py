from src.util import cw_meta
from src.util.listen_lesson import ListenLesson


class Listen1E(ListenLesson):
	def __init__(self):
		super().__init__()
		self.lesson_title = f"E: {cw_meta.formatted('E')}"
		self.lesson_description = f"The letter 'E' is represented with a short press of the CW key. Pause before sending" \
			f" the next letter to indicate you are starting a new letter."

		self.target_text = 'EEEE'

	def key_event(self, cw_text):
		cw_text = re.sub("[^E]", '', cw_text)
		return cw_text
