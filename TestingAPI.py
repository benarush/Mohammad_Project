import requests
import json


def get_token():
    username = "Admin"
    password = "Aa12Aa12"
    post_data = {'username': username, 'password': password}
    r = requests.post('http://127.0.0.1:8000/login/', data=post_data)
    response = json.loads(r.text)
    if "token" in response.keys():
        return response["token"]
    return response["non_field_errors"]


def create_post(token):
    data = {
    "title": "Test_title",
    "content": "Test Content",
    }
    response = requests.post('http://127.0.0.1:8000/postAPI/',
                             headers={'Authorization': 'Token ' + token},
                             data=data)
    print(response.text)


def create_post_likes(token):
    data = {
    "post": 944
    }
    response = requests.post('http://127.0.0.1:8000/post_like/',
                             headers={'Authorization': 'Token ' + token},
                             data=data)
    return response.text

def create_user():
    data = {
        "username": "TestUserdsa",
        "password": "Aa12Aa12",
        "email": "dudu@fdsfds.com"
    }
    response = requests.post('http://127.0.0.1:8000/create_user/',
                             data=data)
    print(response.text)


def update_post(token):
    data = {
        "post_id": "944",
        "title": "3333332",
        "content": "Its Work222222!!!",
    }
    response = requests.put('http://127.0.0.1:8000/postAPI/',
                             headers={'Authorization': 'Token ' + token},
                             data=data)
    return response.text


def delete_post(token):
    data = {"post_id": "945"}
    response = requests.delete('http://127.0.0.1:8000/postAPI/',
                             headers={'Authorization': 'Token ' + token},
                             data=data
                             )
    return response.text


def get_posts(token):
    response = requests.get('http://127.0.0.1:8000/postAPI/',
                               headers={'Authorization': 'Token ' + token},
                               )
    return json.dumps(json.loads(response.text), indent=2)


token = get_token()
print(f"Token - {token}")
# print(get_posts(token))
# print(create_post(token))
#print(create_post_likes(token))
#print(update_post(token))
#print(delete_post(token))
# create_user()

