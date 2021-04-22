class Lesson:
	def __init__(self):
		self.lesson_description = ''
		self.target_text = ''

	def key_event(self, cw_textbox):
		# this method is for any pre-processing or adjusting that needs to be done during the lesson.
		raise Exception("Base method cannot be called!")

	def is_complete(self, cw_text):
		# return true/false if the lesson is completed or not
		raise Exception("Base method cannot be called!")
