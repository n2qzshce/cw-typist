import difflib
import logging
from threading import Thread

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
		self._beat_interval = 100
		self._play_button = play_button
		self._submit_button = submit_button
		self._tone_events = list()
		registry = ListeningLessonRegistry()
		super().__init__(registry=registry, lesson_description_box=lesson_description_box)

	def load_lesson(self):
		self.stop_message()
		super().load_lesson()
		self.input_box.text = ''
		self._score_report.text = ''
		self._play_button.disabled = False
		self._submit_button.disabled = False

	def play_message(self):
		if self._lesson.is_quiz():
			self._play_button.disabled = True

		def focus_text(_): self.input_box.focus = True
		Clock.schedule_once(focus_text, 1/10)

		cw_sequence = cw_meta.build_sequence(self._lesson.target_text)
		start_duration = list()
		total_millis = 1000

		for x in cw_sequence:
			millis = cw_meta.symbol_ms(cw_meta.wpm(cw_meta.starting_rate), x)
			if x == cw_meta.DIT or x == cw_meta.DAH:
				start_duration.append((total_millis, millis))
			total_millis += millis + self._beat_interval

		x = 0
		for k in start_duration:
			thread = Thread(target=lambda : self.schedule_tone(x, k[0], k[1]))
			thread.start()

	def schedule_tone(self, x, wait_ms, duration_ms):
		logging.debug(f"Scheduling tone {x} in {wait_ms} for {duration_ms}")
		self._tone_events.append(Clock.schedule_once(lambda _: self.play_tone(), wait_ms/1000))
		self._tone_events.append(Clock.schedule_once(lambda _: self.stop_tone(), (wait_ms+duration_ms)/1000))

	def play_tone(self):
		logging.debug(f"Playing tone!")
		self._sound.play()
		self._sound_indicator.rgb = (0.0, 0.8, 0.0)

	def stop_tone(self):
		logging.debug(f"Stopping tone!")
		self._sound.stop()
		self._sound_indicator.rgb = (0.4, 0.4, 0.4)

	def stop_message(self):
		for x in self._tone_events:
			x.cancel()

		self.stop_tone()
		self._tone_events = list()

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

