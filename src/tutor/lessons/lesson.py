class Lesson:
	def __init__(self):
		self.lesson_description = ''
		self.target_text = ''

	def key_event(self, cw_textbox):
		raise Exception("Base method cannot be called!")
