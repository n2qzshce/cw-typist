class LayoutIds:
	action_previous = 'action_previous'
	clear_text = 'clear_text'
	cw_lesson = 'cw_lesson'
	cw_output = 'cw_output'
	cw_button = 'cw_button'
	exit_button = 'exit_button'
	lesson_description = 'lesson_description'
	lesson_next = 'lesson_next'
	lesson_prev = 'lesson_prev'
	nothing_button = 'nothing_button'
	toggle_mute = 'toggle_mute'
	wpm_display = 'wpm_display'


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
					id: {LayoutIds.toggle_mute}
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
		orientation: "horizontal"
		BoxLayout:
			padding: dp(20)
			orientation: "vertical"
			Label:
				text: 'Lesson'
				size_hint_y: 0.075
			Label:
				id: {LayoutIds.cw_lesson}
				font_name: 'SourceCodePro'
				text: ''
				size_hint: (1, 0.5)
				readonly: True
				font_size: dp(11)
				markup: True
			Label:
				text: 'Your Input'
				size_hint_y: 0.075
			TextInput:
				id: {LayoutIds.cw_output}
				font_name: 'SourceCodePro'
				text: ''
				size_hint: (1, 0.5)
				readonly: True
				font_size: dp(11)
		BoxLayout:
			padding: dp(40)
			orientation: "vertical"
			BoxLayout:
				padding: dp(10)
				size_hint: (1.0, 0.2)
				orientation: "horizontal"
				Button:
					id: {LayoutIds.clear_text}
					text: 'Clear output'
					font_size: dp(14)
			Button:
				id : {LayoutIds.cw_button}
				text: 'CW Key'
				font_size: dp(14)
			Label:
				size_hint: (1, 0.1)
				id: {LayoutIds.wpm_display}
				text_size: self.width, None
				text: 'WPM: NaN'
		BoxLayout:
			orientation: "vertical"
			BoxLayout:
				size_hint: (1, 0.2)
				padding: dp(10)
				Button:
					id: {LayoutIds.lesson_prev}
					text: 'Previous lesson'
					font_size: dp(14)
				Button:
					id: {LayoutIds.lesson_next}
					text: 'Next lesson'
					font_size: dp(14)
			Label:
				id: {LayoutIds.lesson_description}
				text_size: self.width, None
				size_hint: (1, 0.3)
				text: ''
				markup: True
			Label:
				size_hint: (1, 0.4)
"""