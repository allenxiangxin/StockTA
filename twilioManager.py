import json
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse

class twilioManager:

    client = ''
    my_id = ''
    twilio_id = ''

    def __init__(self, token_file='private_info/twilio_token.json'):
        with open (token_file, "r") as f:
            data = json.load(f)
            auth_token = data['token']
            account_sid = data['sid']
            self.client = Client(account_sid, auth_token)
            self.my_id = data['me']
            self.twilio_id = data['twilio']

    def send_whatsapp_alarm(self, main_text):
        message = self.client.messages.create(
                                         from_=self.twilio_id['whatsapp'],
                                         body=main_text,
                                         to=self.my_id['whatsapp'])

    def send_text_alarm(self, main_text):
        message = self.client.messages.create(
                                         from_=self.twilio_id['text'],
                                         body=main_text,
                                         to=self.my_id['text'])


class Dog:

    kind = 'canine'         # class variable shared by all instances

    def __init__(self, name):
        self.name = name    # instance variable unique to each instance


    # def reply_msg():
    #     response = MessagingResponse()
    #     message = Message()
    #     message.body(main_text)
    #     response.append(message)
    #     response.redirect('https://demo.twilio.com/welcome/sms/')
    #     print(response)
    #     print(message.sid)
