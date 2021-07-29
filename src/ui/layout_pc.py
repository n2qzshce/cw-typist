class LayoutIds:
	action_previous = 'action_previous'
	content_panel = 'content_panel'
	exit_button = 'exit_button'
	nothing_button = 'nothing_button'
	switch_lesson_write = 'switch_lesson_write'
	switch_lesson_read = 'switch_lesson_read'


class ListenLayoutIds:
	answer_input = 'answer_input'
	cw_button = 'cw_button'
	cw_lesson = 'cw_lesson'
	lesson_prev = 'lesson_prev'
	lesson_next = 'lesson_next'
	lesson_description = 'lesson_description'
	listen_again = 'listen_again'

	listen_lesson_panel = 'listen_lesson_panel'
	listen_submit = 'listen_submit'
	queue_light = 'queue_light'
	wpm_display = 'wpm_display'


class WriteLayoutIds:
	cw_button = 'cw_button'
	cw_output = 'cw_output'
	cw_lesson = 'cw_lesson'
	clear_text = 'clear_text'
	lesson_description = 'lesson_description'
	lesson_next = 'lesson_next'
	lesson_prev = 'lesson_prev'
	listen_submit = 'listen_submit'
	listen_lesson_panel = 'listen_lesson_panel'
	listen_again = 'listen_again'
	toggle_mute = 'toggle_mute'
	wpm_display = 'wpm_display'
	write_lesson_panel = 'write_lesson_panel'


write_lesson_panel = f"""
BoxLayout:
	id: {WriteLayoutIds.write_lesson_panel}
	orientation: "horizontal"
	BoxLayout:
		padding: dp(20)
		orientation: "vertical"
		Label:
			text: 'Lesson'
			size_hint_y: 0.075
		StackLayout:
			id: {WriteLayoutIds.cw_lesson}
			size_hint: (1, 0.5)
		Label:
			text: 'Your Input'
			size_hint_y: 0.075
		TextInput:
			id: {WriteLayoutIds.cw_output}
			font_name: 'SourceCodePro'
			text: ''
			size_hint: (1, 0.5)
			readonly: True
			font_size: dp(13)
	BoxLayout:
		padding: dp(40)
		orientation: "vertical"
		BoxLayout:
			padding: dp(10)
			size_hint: (1.0, 0.2)
			orientation: "horizontal"
			Button:
				id: {WriteLayoutIds.clear_text}
				text: 'Clear output'
				font_size: dp(16)
		Button:
			id : {WriteLayoutIds.cw_button}
			text: 'CW Key'
			font_size: dp(16)
		Label:
			size_hint: (1, 0.1)
			id: {WriteLayoutIds.wpm_display}
			text_size: self.width, None
			text: 'WPM: NaN'
	BoxLayout:
		orientation: "vertical"
		BoxLayout:
			size_hint: (1, 0.2)
			padding: dp(12)
			Button:
				id: {WriteLayoutIds.lesson_prev}
				text: 'Previous lesson'
				font_size: dp(16)
			Button:
				id: {WriteLayoutIds.lesson_next}
				text: 'Next lesson'
				font_size: dp(16)
		Label:
			id: {WriteLayoutIds.lesson_description}
			text_size: self.width, None
			padding: (dp(12), dp(12))
			size_hint: (1, 0.3)
			text: ''
			markup: True
		Label:
			size_hint: (1, 0.4)
"""

listen_lesson_panel = f"""
BoxLayout:
	id: {ListenLayoutIds.listen_lesson_panel}
	orientation: "horizontal"
	BoxLayout:
		padding: dp(20)
		orientation: "vertical"
		Label:
			id: {ListenLayoutIds.cw_lesson}
			size_hint: (1, 0.15)
		Label:
			text: 'Your Input'
			size_hint_y: 0.075
		TextInput:
			id: {ListenLayoutIds.answer_input}
			font_name: 'SourceCodePro'
			text: ''
			size_hint: (1, 0.5)
			font_size: dp(13)
		Button:
			id: {ListenLayoutIds.listen_submit}
			text: 'Submit'
			font_size: dp(16)
			size_hint: (1, 0.15)
	BoxLayout:
		padding: dp(40)
		orientation: "vertical"
		BoxLayout:
			padding: dp(10)
			size_hint: (1.0, 0.2)
			orientation: "horizontal"
			Button:
				id: {ListenLayoutIds.listen_again}
				text: 'Play Message'
				font_size: dp(16)
		AnchorLayout:
			size_hint: (1.0, 0.8)
			anchor_x: 'center'
			anchor_y: 'center'
			canvas:
				Ellipse:
					size: min(self.size)*0.66, min(self.size)*0.66
					pos: self.center_x - min(self.size) * 0.33, self.center_y - min(self.size) * 0.33
		Label:
			size_hint: (1, 0.1)
			id: {ListenLayoutIds.wpm_display}
			text_size: self.width, None
			text: 'WPM: NaN'
	BoxLayout:
		orientation: "vertical"
		BoxLayout:
			size_hint: (1, 0.2)
			padding: dp(12)
			Button:
				id: {ListenLayoutIds.lesson_prev}
				text: 'Previous lesson'
				font_size: dp(16)
			Button:
				id: {ListenLayoutIds.lesson_next}
				text: 'Next lesson'
				font_size: dp(16)
		Label:
			id: {ListenLayoutIds.lesson_description}
			text_size: self.width, None
			padding: (dp(12), dp(12))
			size_hint: (1, 0.3)
			text: ''
			markup: True
		Label:
			size_hint: (1, 0.4)
"""

kv = f"""
BoxLayout:
	orientation: "vertical"
	ActionBar:
		ActionView:
			ActionPrevious:
				id: {LayoutIds.action_previous}
				title: 'CW Typist'
				with_previous: False
				enabled: False
			ActionButton:
				id: {LayoutIds.switch_lesson_write}
				text: "Write Mode"
			ActionButton:
				id: {LayoutIds.switch_lesson_read}
				text: "Read Mode"
			ActionSeparator:
				important: True
			ActionGroup:
				text: "File"
				mode: "spinner"
				dropdown_width: dp(225)
				ActionButton:
					id: {LayoutIds.exit_button}
					text: "Exit"
			ActionGroup:
				text: "Sound"
				mode: "spinner"
				ActionToggleButton:
					id: {WriteLayoutIds.toggle_mute}
					text: "Toggle mute"
					#state: 'down'
			ActionGroup:
				text: "Help / Getting Started"
				mode: "spinner"
				dropdown_width: dp(250)
				ActionButton:
					id: {LayoutIds.nothing_button}
					text: "Warning: pointless button"
	BoxLayout:
		id: {LayoutIds.content_panel}
"""
