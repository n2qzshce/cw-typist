from src.tutor.lessons.lib.listening_lesson_registry import ListeningLessonRegistry
from src.tutor.tutor import Tutor
from kivy.clock import Clock

from src.util import cw_meta


class ListeningTutor(Tutor):
	def __init__(self, cw_textbox, lesson_description_box, sound, sound_indicator):
		self.cw_textbox = cw_textbox
		self._sound = sound
		self._sound_indicator = sound_indicator
		self._clocks = list()
		self._beat_interval = 50
		registry = ListeningLessonRegistry()
		super().__init__(registry=registry, lesson_description_box=lesson_description_box)
		pass

	def load_lesson(self):
		super().load_lesson()
		pass

	def play_message(self):
		cw_sequence = cw_meta.build_sequence(self._lesson.target_text)
		start_duration = dict()
		total_millis = 0
		millis = 0
		for x in cw_sequence:
			millis = cw_meta.symbol_ms(cw_meta.wpm(cw_meta.starting_rate), x)
			if x == cw_meta.DIT or x == cw_meta.DAH:
				start_duration[total_millis] = millis
			total_millis += millis + self._beat_interval

		for k in start_duration.keys():
			the_player = lambda x: self.play_tone(start_duration[k])
			Clock.schedule_once(the_player, k / 1000)

	def play_tone(self, duration_ms):
		self._sound.play()
		Clock.schedule_once(self.stop_tone, duration_ms / 1000)

	def stop_tone(self, _):
		self._sound.stop()

	def tone_done(self):
		pass
