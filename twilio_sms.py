
# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


def send_text(in_body):
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = 'AC58f30788e20407de4b896d80fe8a4f00'
    auth_token = '8037e390e1b0215a90fd9ad53f7aba58'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
                body=in_body,
                from_='+15172450874',
                to='+14088322687'
                )

    print(message.body)
    return message.body

if __name__ == '__main__':
    send_text()
