from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import socket
import threading

from client import thread_sending, thread_receiving

nickname = input("Choose your nickname : ").strip()
while not nickname:
    nickname = input("Your nickname should not be empty : ").strip()
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"  # "127.0.1.1"
port = 8000
my_socket.connect((host, port))


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
        message_with_nickname = nickname + " : " + message
        my_socket.send(message_with_nickname.encode())
        self.input_field.text = ""
        label = Label(text=message, size_hint_y=None, height=30, text_size=(self.width, None),
                      halign='left', valign='middle')
        self.text_box.add_widget(label)

    def receive_message(self, message):
        message = "  " + message
        label = Label(text=message, size_hint_y=None, height=30, text_size=(self.width, None),
                      halign='right', valign='middle')
        self.text_box.add_widget(label)


class ChatApp(App):
    def build(self):
        return ChatWindow()


thread_send = threading.Thread(target=thread_sending)
thread_receive = threading.Thread(target=thread_receiving)
thread_send.start()
thread_receive.start()

if __name__ == "__main__":
    ChatApp().run()
