from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import tkinter as tk
import threading
from tkinter_colors import COLORS
import random
import re
from profanity_check import predict, predict_prob
from matplotlib import colors
import colorsys
app = Flask(__name__)


class App(threading.Thread):

    def __init__(self):
        self.bg_color = '#ffffff'
        self.fg_color=''
        self.default_message = "vikingsdev.ca/signup"
        # backup num: +1 (604)-901-6042
        self.phone_num = "+1 (604)-359-3028"
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def set_colour(self, color):
        self.root.configure(bg=color)
        self.bg_color = color
        self.label.configure(bg=self.bg_color)
        self.label.pack(side='top', expand='yes', fill='both')
        self.lastnum.configure(bg=self.bg_color)
        self.message.configure(bg=self.bg_color)

        r,g,b = colors.to_rgb(self.bg_color)
        if colorsys.rgb_to_hls(r,g,b)[1] >= 0.175:
            self.fg_color = '#000000'
        if colorsys.rgb_to_hls(r,g,b)[1] <= 0.1833:
            self.fg_color = '#ffffff'
        self.label.configure(fg=self.fg_color)
        self.lastnum.configure(fg=self.fg_color)
        self.message.configure(fg=self.fg_color)

    def set_lastnumber(self, phone_number):
        self.lastnum.configure(text="Last phone number: " + phone_number)
        self.lastnum.pack(side='top', expand='yes', fill='both')

    def set_message(self, message):
        self.message.configure(text='Public Message:' + '\n' + message)
        self.message.pack(side='top', expand='yes', fill='both')

    def reset_message(self):
        self.message.configure(text=self.default_message)
        self.message.pack(side='top', expand='yes', fill='both')

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.configure(bg=self.bg_color)
        self.label = tk.Label(self.root, text="Text a colour to "+self.phone_num+" to change it, \nor type a message.",
                              font=("Acre", 40), bg=self.bg_color, anchor='center')
        self.label.pack(side='top', expand='yes', fill='both')
        self.lastnum = tk.Label(self.root, text="Last phone number: -", font=("Acre", 40),
                                bg=self.bg_color, anchor='center')
        self.lastnum.pack(side='top', expand='yes', fill='both')
        self.message = tk.Label(self.root, text=self.default_message, font=("Acre", 40),
                                bg=self.bg_color, anchor='center')
        self.message.pack(side='top', expand='yes', fill='both')
        self.root.attributes("-fullscreen", True)

        self.root.mainloop()


tkapp = App()


@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    number = request.form['From']
    message_body = request.form['Body']
    print(number)
    print(message_body)
    hex_match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', message_body.lower())
    if message_body.lower() not in colors.get_named_colors_mapping() and not hex_match:
        if predict([message_body])[0] < 0.7:
            App.set_message(self=tkapp, message=message_body)
        if message_body.lower == '/r':
            App.reset_message()
        message_body = random.choice(list(colors.get_named_colors_mapping().values()))
    elif not hex_match:
        message_body = colors.get_named_colors_mapping()[message_body.lower()]

    App.set_colour(self=tkapp, color=message_body)
    App.set_lastnumber(self=tkapp, phone_number=number)
    return None


if __name__ == "__main__":
    app.run(debug=True)
