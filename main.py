import re
import json
import string
import random
import requests

endpoint = 'https://api.mail.tm'
token: str = ''


def domains():
    response = requests.get(endpoint + '/domains').json()
    return response['hydra:member'][0]['domain']


def random_pass():
    length = 12
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def random_credentials():
    return {'email': random_pass() + '@' + domains(), 'password': random_pass()}


def register():
    email = random_credentials()['email']
    password = random_credentials()['password']
    payload = {'address': email, 'password': password}
    headers = {'Content-Type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    response = requests.post(endpoint + '/accounts', headers=headers, data=json.dumps(payload)).json()
    dados = {'id': response['id'], 'email': response['address'], 'password': password}
    return dados


def token_email(email, password):
    payload = {'address': email, 'password': password}
    headers = {'Content-Type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    response = requests.post(endpoint + '/token', headers=headers, data=json.dumps(payload)).json()
    return response['token']


def get_messages(token):
    headers = {'Content-Type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
               'Authorization': 'Bearer {}'.format(token)}

    response = requests.get("{}/messages?page={}".format(endpoint, 1), headers=headers).json()
    messages = []
    for message_data in response["hydra:member"]:
        response = requests.get("{}/messages/{}".format(endpoint, message_data['id']), headers=headers).json()["text"]
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, response)
        for x in url:
            messages = {'url': x[0]}

    return messages


def create_account(email, password):
    payload = {'email': email, 'password': password}
    headers = {'Content-Type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
               'Accept': 'application/json, text/plain, */*'}
    response = requests.post('https://lampyre.io/api/1.6/accounts', headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        print('Conta Criada\n')
        print(f"Email: {email}", f"\nPassword: {password}", f"\nUrl:{get_messages(token)['url']}")
    else:
        print('algum erro')


credentials = register()

token = token_email(credentials['email'], credentials['password'])
create_account(credentials['email'], credentials['password'])
