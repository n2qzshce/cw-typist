import difflib
import re

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.label import Label

from src.cw.SymbolTracker import SymbolTracker
from src.tutor.lessons.lib.lesson_registry import LessonRegistry
from src.util import cw_meta


class WritingTutor:
	def __init__(self, cw_textbox, lesson_textbox, lesson_description_box):
		self._registry = LessonRegistry()
		self.cw = SymbolTracker()
		self.cw_textbox = cw_textbox
		self._lesson_textbox = lesson_textbox
		self._lesson_description_box = lesson_description_box
		self._lesson = None
		self._next_letter_event = Clock.schedule_once(self._next_letter, self.cw.next_letter_timing())
		self._next_letter_event.cancel()
		self._next_word_event = Clock.schedule_once(self._next_word, self.cw.next_word_timing())
		self._next_word_event.cancel()
		self._lesson_already_completed = False

		self._lesson_number = 4
		self.load_lesson()

	def cw_down(self, tick):
		self.cw.keyed_down(tick)
		self.key_event()
		self._next_letter_event.cancel()
		self._next_word_event.cancel()

	def cw_up(self, tick):
		self.cw.keyed_up(tick)
		self.key_event()
		self._next_letter_event()
		self._next_word_event()

	def _next_letter(self, event):
		self.cw_textbox.text += self.cw.next_letter()
		Clock.unschedule(self._next_letter_event)
		self.key_event()

	def _next_word(self, event):
		self.cw_textbox.text += cw_meta.cw_printed[cw_meta.NEXT_WORD]
		Clock.unschedule(self._next_word_event)
		self.key_event()

	def load_lesson(self):
		self._lesson_textbox.clear_widgets()
		self._lesson_number = self._lesson_number % len(self._registry.lessons)
		self._lesson = self._registry.lessons[self._lesson_number]()
		self._lesson_description_box.text = f"[b]{self._lesson.lesson_title}[/b]\n\n{self._lesson.lesson_description}"
		self._lesson_textbox.text = self._lesson.target_text
		self._lesson_already_completed = False
		self.cw_textbox.text = ''
		if self._lesson.is_quiz():
			self.cw_textbox.password = True
		else:
			self.cw_textbox.password = False
		self.key_event()

	def lesson_next(self):
		self._lesson_number += 1
		self.load_lesson()

	def lesson_prev(self):
		self._lesson_number -= 1
		self.load_lesson()

	def reset_lesson(self):
		self.load_lesson()

	def key_event(self):
		if self._lesson_already_completed or self._lesson_number == 0:
			return

		update_text = self._lesson.key_event(self.cw_textbox.text)
		self.cw_textbox.text = update_text
		self._set_lesson_text()

		if self._lesson.is_complete(self.cw_textbox.text):
			self.complete_lesson()
			return
		if len(self.cw_textbox.text) >= len(self._lesson.target_text):
			self.display_accuracy()
			return
		pass

	def _correct_bad_space_and_get_char_index(self):
		current_char = min(len(self._lesson.target_text) - 1, len(self.cw_textbox.text))
		if current_char <= 0:
			return current_char

		if len(self._lesson.target_text) == len(self.cw_textbox.text):
			return current_char

		target_char = self._lesson.target_text[current_char]
		if target_char == ' ' and self.cw_textbox.text[-1] == ' ':
			self.cw_textbox.text += ' '
			current_char += 1

		return current_char

	def complete_lesson(self):
		if self._lesson_already_completed:
			return
		self.cw_textbox.password = False
		self._lesson_already_completed = True
		self.display_conclusion_flavortext("Good job!")
		self.cw_textbox.text += "\n"

	def display_accuracy(self):
		if self._lesson_already_completed:
			return
		self._lesson_already_completed = True
		self.cw_textbox.password = False
		diff = difflib.SequenceMatcher(a=self._lesson.target_text, b=self.cw_textbox.text)
		match_pct = diff.ratio() * 100
		self.display_conclusion_flavortext(f"\nLesson complete.\nAccuracy: {match_pct:2.0f}%")

		if self._lesson.is_quiz():
			flavor_text = "They missed your message! Try again?"
			if match_pct > 90:
				flavor_text = "A few typos, but you nailed it."
			self.display_conclusion_flavortext(f"\n{flavor_text}")
		return

	def _set_lesson_text(self):
		self._lesson_textbox.clear_widgets()

		lesson_text = self._lesson.target_text
		current_char = self._correct_bad_space_and_get_char_index()

		split = lesson_text.split(' ')

		ordered_children = list()
		for i in split:
			label = Label(
				text=i+' ',
				font_size=dp(18),
				font_name='SourceCodePro',
				markup=True,
			)
			label.size_hint = (None, 0.1)
			label.size_hint_max_y = label.text_size[1]
			label.size = label.texture_size
			label.width = dp(12) * len(i) + dp(12)
			self._lesson_textbox.add_widget(label)
			ordered_children.append(label)

		chars_count = 0
		for i in ordered_children:
			if self._lesson.is_quiz():
				break
			if chars_count + len(i.text) > current_char:
				in_str_index = current_char - chars_count
				replace_text = f"{i.text[:in_str_index]}" \
								f"[u]{i.text[in_str_index]}[/u]" \
								f"{i.text[in_str_index + 1:]}"
				i.text = replace_text
				break
			chars_count += len(i.text)
		return

	def display_conclusion_flavortext(self, text):
			label = Label(
				text=text,
				font_size=dp(18),
				markup=True,
				color=[0.90, 0.90, 0.10, 1.0]
			)
			label.size_hint_x = 1
			label.padding_y = dp(18)
			self._lesson_textbox.add_widget(label)

