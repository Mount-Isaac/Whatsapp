import requests as r
import json
from prettytable import PrettyTable
import os
from dotenv import load_dotenv


class sendWhatsappMessagesApi:
    # Automate sending Whatsapp message using the Whatsapp Official API
    def __init__(self, token,  phone, message):
        self.token= token
        self.phone = phone
        self.message = message

    
    def send_message(self, url):
        pre_payload = f'token={self.token}&to={self.phone}&body={self.message}'

        # payload 
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.payload = pre_payload.encode('utf8').decode('iso-8859-1')
        self.response = r.post(url, data=self.payload, headers=self.headers)
        status_info = self.response.text
        return status_info

    def get_messages(self, url):
        self.response = r.get(url)
        
        # convert messages JSON object to a python dict
        messages = json.loads(self.response.text)

        # format the output
        table = PrettyTable(['Id', 'Reference Id', 'From', 'To', 'Body', 'Priority', 'Status', 'Ack', 'Type', 'Created', 'Sent', 'Metadata'])

        # add the messages in the table
        for element in messages.get('messages'):
            table.add_row([x for x in list(element.values())])

        return table


# load local environment where tokens are stored
load_dotenv()
token = os.getenv('TOKEN')
instance = os.getenv("INSTANCE")

'''
paramter formats
phone='+254759856000'
message = 'Hello, motherfucker :)'
'''

# Take phone number
country_code = str(input("Enter your country code: "))
number = str(input('Enter the phone number to receive the message: '))
phone = f'+{country_code}{number}'

# Take message 
message = str(input("Enter the message being sent: "))

# URLS
send_message_url = f"https://api.ultramsg.com/{instance}/messages/chat"
get_messags_url = f'https://api.ultramsg.com/{instance}/messages?token={token}&page=1&limit=100'



# Whatsapp Class API message instance
whatsapp_api_messager = sendWhatsappMessagesApi(token, phone, message)

# send a message
print('sending your message...')
print(whatsapp_api_messager.send_message(send_message_url))

print('\nRetrieving your messages...')
# retrieve all the messages
print(whatsapp_api_messager.get_messages(get_messags_url))
