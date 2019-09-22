# twilio-screen
A small python app that changes colour whenever you text a twilio number.

## Features
* Shows the latest number that texted it
* Can show public messages
* Takes string input to change the color, for example you can text 'blue' and the screen will change correspondingly
* Has a profanity filter for public messages!
* If the texted content is not a valid colour, a random colour is chosen.
* Automatically changes the text colour to be readable depending on the background

# Installation

Install dependencies:
```
pip3 install flask
sudo apt-get install python3-tk
pip3 install profanity-check
```

# Running
Open a terminal and run:
```
git clone https://github.com/FrankWhoee/twilio-screen.git
cd twilio-screen
./ngrok http 5000
```

Get the ngrok link and add /sms to the end of it, so for example:
`http://353c8600.ngrok.io/sms`
Go to your twilio console and add this link to the webhooks. Then run:

```
python3 app.py
```
