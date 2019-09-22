from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import tkinter as tk
import threading
from tkinter_colors import COLORS
import random
import re
from profanity_check import predict, predict_prob

app = Flask(__name__)

class App(threading.Thread):

    def __init__(self):
        self.bg_color = 'snow'
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def set_colour(self,color):
        self.root.configure(bg=color)
        self.bg_color = color
        self.label.configure(bg= self.bg_color)
        self.label.pack(side='top', expand='yes', fill='both')
        self.lastnum.configure(bg=self.bg_color)
        self.message.configure(bg=self.bg_color)

    def set_lastnumber(self, phone_number):
        self.lastnum.configure(text="Last phone number: " + phone_number)
        self.lastnum.pack(side='top', expand='yes', fill='both')

    def set_message(self, message):
        self.message.configure(text='Public Message:' + '\n' + message)
        self.message.pack(side='top', expand='yes', fill='both')

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.configure(bg=self.bg_color)
        self.label = tk.Label(self.root, text="Text a colour to PHONE_NUMBER to change it, or type a message.", font=("Acre",40), bg=self.bg_color, anchor='center')
        self.label.pack(side='top', expand='yes', fill='both')
        self.lastnum = tk.Label(self.root, text="Last phone number: -", font=("Acre", 40),
                                bg=self.bg_color, anchor='center')
        self.lastnum.pack(side='top', expand='yes', fill='both')
        self.message = tk.Label(self.root, text="vikingsdev.ca/signup", font=("Acre", 40),
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
    if message_body.lower() not in COLORS and not hex_match:
        if predict([message_body])[0] < 0.7:
            App.set_message(self=tkapp, message=message_body)
        message_body = random.choice(COLORS)
    App.set_colour(self=tkapp, color=message_body.lower())
    App.set_lastnumber(self=tkapp, phone_number=number)
    return None

if __name__ == "__main__":
    app.run(debug=True)





