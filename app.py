from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock

global chat_window


class ChatWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.text_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.text_box.bind(minimum_height=self.text_box.setter('height'))
        self.scroll.add_widget(self.text_box)

        self.input_and_button = BoxLayout(size_hint=(1, 0.1), pos_hint={'y': 0})
        self.input_field = TextInput(size_hint=(0.9, 1), multiline=False)
        self.send_button = Button(text="Send", size_hint=(0.1, 1))
        self.input_and_button.add_widget(self.input_field)
        self.input_and_button.add_widget(self.send_button)

        self.send_button.bind(on_press=self.send_message)
        self.add_widget(self.scroll)
        self.add_widget(self.input_and_button)
        self.input_field.bind(on_text_validate=self.send_message)

    def send_message(self, instance):
        message = "  You:  " + self.input_field.text
        self.input_field.text = ""
        label = Label(text=message, size_hint_y=None, height=30, text_size=(self.width, None),
                      halign='left', valign='middle')
        self.text_box.add_widget(label)

    def recieve_message(self, instance, name, msg):
        message = f"{name}:  " + msg + "  "
        self.input_field.text = ""
        label = Label(text=message, size_hint_y=None, height=30, text_size=(self.width, None),
                      halign='right', valign='middle')
        self.text_box.add_widget(label)


class ChatApp(App):
    def build(self):
        global chat_window
        chat_window = ChatWindow()
        Clock.schedule_interval(self.process_loop, 0.1)
        return chat_window

    def process_loop(self, dt):
        tick()


def tick():
    global chat_window
    # chat_window.recieve_message(None, "rkasti", "Hello")


if __name__ == "__main__":
    chat_window = None
    ChatApp().run()
