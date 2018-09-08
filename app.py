
# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from flask import Flask
app = Flask(__name__)

@app.route("/sms")
def send_text():
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = 'AC58f30788e20407de4b896d80fe8a4f00'
    auth_token = '8037e390e1b0215a90fd9ad53f7aba58'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
                body='This is the ship that made the Kessel Run in fourteen parsecs?',
                from_='+15172450874',
                to='+15174025378'
                )

    print(message.body)
    return message.body


if __name__ == "__main__":
    app.run(debug=True)