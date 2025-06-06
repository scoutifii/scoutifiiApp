import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = '17084b139e3e43928cea71ee5c2aa494'
auth_token = '17084b139e3e43928cea71ee5c2aa494'
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def send_sms(user_code, phone_no):
     message = client.messages \
                     .create(
                          body=f'{user_code} verification code from Scoutifii.',
                          from_='+256773405024',
                          to=f'{phone_no}'
                      )

print(message.sid)