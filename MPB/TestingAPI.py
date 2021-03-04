import requests
import json

def get_token():
    username = "AVA"
    password = "Aa12Aa12"
    post_data = {'username': username, 'password': password}
    r = requests.post('http://127.0.0.1:8000/login/', data=post_data)
    response = json.loads(r.text)
    if "token" in response.keys():
        return response["token"]
    return response["non_field_errors"]

def create_post(token):
    data = {
    "title": "Bla Bla555",
    "content": "yoo yooo5555",
    }
    response = requests.post('http://127.0.0.1:8000/create_post/',
                             headers={'Authorization': 'Token ' + token},
                             data=data)
    print(response.text)


def create_post_likes(token):
    data = {
    "post": 6
    }
    response = requests.post('http://127.0.0.1:8000/post_like/',
                             headers={'Authorization': 'Token ' + token},
                             data=data)
    print(response.text)

def create_user():
    data = {
        "username": "TestUserdsa",
        "password": "Aa12Aa12",
        "email": "dudu@fdsfds.com"
    }
    response = requests.post('http://127.0.0.1:8000/create_user/',
                             data=data)
    print(response.text)

# token = get_token()
# print(f"token - {token}")
# print(create_post(token))
# print(create_post_likes(token))
# create_user()

