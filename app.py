import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import socket

global chat_window, nickname, message_r
nickname = input("Choose your nickname: ").strip()


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
        message = f"  {nickname}:  " + self.input_field.text
        my_socket.send(message.encode())
        self.input_field.text = ""
        label = Label(text=message, size_hint_y=None, height=30, text_size=(self.width, None),
                      halign='left', valign='middle')
        self.text_box.add_widget(label)

    def receive_message(self):
        global message_r
        if message_r != "":
            label = Label(text=message_r, size_hint_y=None, height=30, text_size=(self.width, None),
                          halign='right', valign='middle')
            self.text_box.add_widget(label)
            message_r = ""


def thread_receiving():
    global message_r
    message_r = my_socket.recv(1024).decode() + "  "


class ChatApp(App):
    def build(self):
        global chat_window
        chat_window = ChatWindow()
        Clock.schedule_interval(self.process_loop, 0.1)
        return chat_window

    def process_loop(self, dt):
        global chat_window, x
        if x > 10:
            chat_window.receive_message()
            x = 0
        x += 1


if __name__ == "__main__":
    global nicknames, x

    x = 0

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.1.1"  # "127.0.1.1"
    port = 8000
    my_socket.connect((host, port))

    message_r = ""

    thread_receive = threading.Thread(target=thread_receiving)
    thread_receive.start()

    ChatApp().run()
