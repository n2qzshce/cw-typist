import difflib

from src.tutor.lessons.lib.listening_lesson_registry import ListeningLessonRegistry
from src.tutor.tutor import Tutor
from kivy.clock import Clock

from src.util import cw_meta


class ListeningTutor(Tutor):
	def __init__(self, input_box, score_report, lesson_description_box, sound, sound_indicator, play_button, submit_button):
		self.input_box = input_box
		self._score_report = score_report
		self._sound = sound
		self._sound_indicator = sound_indicator
		self._clocks = list()
		self._beat_interval = 50
		self._play_button = play_button
		self._submit_button = submit_button
		registry = ListeningLessonRegistry()
		super().__init__(registry=registry, lesson_description_box=lesson_description_box)
		pass

	def load_lesson(self):
		super().load_lesson()
		self.input_box.text = ''
		self._score_report.text = ''
		self._play_button.disabled = False
		self._submit_button.disabled = False
		pass

	def play_message(self):
		if self._lesson.is_quiz():
			self._play_button.disabled = True

		def focus_text(_): self.input_box.focus = True
		Clock.schedule_once(focus_text, 1/10)

		cw_sequence = cw_meta.build_sequence(self._lesson.target_text)
		start_duration = dict()
		total_millis = 1000

		for x in cw_sequence:
			millis = cw_meta.symbol_ms(cw_meta.wpm(200), x)
			if x == cw_meta.DIT or x == cw_meta.DAH:
				start_duration[total_millis] = millis
			total_millis += millis

		for k in start_duration.keys():
			def the_player(_): self.play_tone(start_duration[k])
			Clock.schedule_once(the_player, k / 1000)

	def play_tone(self, duration_ms):
		self._sound.seek(0)
		self._sound.play()
		self._sound_indicator.rgb = (0.0, 0.8, 0.0)
		Clock.schedule_once(self.stop_tone, duration_ms / 1000)

	def stop_tone(self, _):
		self._sound.stop()
		self._sound_indicator.rgb = (0.4, 0.4, 0.4)

	def submit_answer(self):
		if self._lesson.is_quiz():
			self._submit_button.disabled = True
		diff = difflib.SequenceMatcher(a=self._lesson.target_text, b=self.input_box.text.upper())
		match_pct = diff.ratio() * 100

		answer_text = ""
		if not self._lesson.is_quiz():
			answer_text += f"[color=#FFFFFF]Answer: {self._lesson.target_text}[/color]"

		flavor_text = "QSM(Repeat Last)!! Try again?"
		if match_pct == 100:
			flavor_text = "Perfect!"
		elif match_pct > 90:
			flavor_text = "Pretty close!"
		self._score_report.text = f"{answer_text}\nLesson complete.\nAccuracy: {match_pct:2.0f}%\n\n{flavor_text}\n"

