import twilio_sms
import fire_detect

#Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from flask import Flask
app = Flask(__name__)

@app.route("/sms/")
def twilio_fcn():
    twilio_sms.send_text('Warning: possible wildfire near you!')
    return "Twilio text"

@app.route("/")
def fire_msg():
    fire_detect.fire_info()
    return "Info received"

if __name__ == "__main__":
    app.run(debug=True)
