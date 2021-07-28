class ListenLesson:
	def __init__(self):
		self.lesson_title = Exception("Base method cannot be called")
		self.lesson_description = Exception("Base method cannot be called")
		self.target_text = ''

	def key_event(self, cw_textbox):
		# this method is for any pre-processing or adjusting that needs to be done during the lesson.
		raise Exception("Base method cannot be called!")

	def is_complete(self, cw_text):
		return self.target_text == cw_text

	def is_quiz(self):
		return False
