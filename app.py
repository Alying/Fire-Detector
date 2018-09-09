import twilio_sms
import fire_detect
import bgsb


#Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/sms/")
def twilio_fcn():
    twilio_sms.send_text('Warning: possible wildfire near you!')
    return render_template('index.html')

@app.route("/fire/<vid_no>", methods=['GET', 'POST'])
def fire_msg(vid_no):
    if int(vid_no) % 2 == 0:
        fire_detect.fire_info(vid_no)
    else:
        bgsb.bgsb_info(vid_no)
    return render_template('index.html')

@app.route("/agreement/")
def docusign_agree():  
    import docusign_tools.sig_request
    return "Check your email for fire-monitoring subscription agreement."

   
@app.route("/")
def home():
    return render_template('index.html')





if __name__ == "__main__":
    app.run(debug=True)
