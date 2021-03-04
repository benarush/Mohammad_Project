import os
import requests
import xml.etree.ElementTree as ET
import json
import random
import sys


class BotConfig:
    CONFIG_DIR = os.path.join(os.path.dirname(__file__), "")
    urls = {
        'create_user':  'http://127.0.0.1:8000/create_user/',
        'create_post':  'http://127.0.0.1:8000/create_post/',
        'create_like':  'http://127.0.0.1:8000/post_like/',
        'get_token':    'http://127.0.0.1:8000/login/',
    }

    def __init__(self, filename="botRules.xml"):
        self.filename = filename
        self.config_File = os.path.join(self.CONFIG_DIR, filename)
        self.xmlRoot = ET.parse(self.config_File)
        self.loadConfiguration()

    def loadConfiguration(self):
        self.XML = ET.parse(self.config_File)

    def saveChanges(self):
        self.XML.write(self.config_File)

    def set_number_of_users(self, number_of_users):
        self.XML.getroot().attrib['number_of_users'] = number_of_users

    @property
    def number_of_users(self):
        return int(self.XML.getroot().attrib['number_of_users'])

    def set_max_posts_per_user(self, max_posts_per_user):
        self.XML.getroot().attrib['max_posts_per_user'] = max_posts_per_user

    @property
    def max_posts_per_user(self):
        return int(self.XML.getroot().attrib['max_posts_per_user'])

    def set_max_likes_per_user(self, max_likes_per_user):
        self.XML.getroot().attrib['max_likes_per_user'] = max_likes_per_user

    @property
    def max_likes_per_user(self):
        return int(self.XML.getroot().attrib['max_likes_per_user'])

    def __repr__(self):
        return """
                Config Object purpose is to abstract the work with 
                The Configuration file , can only work with one specific file at time , 
               """

    def __str__(self):
        return f"<Config class - {self.filename}>"


class Bot(BotConfig):
    users_data = {}
    users_token = []
    current_user_posts = []
    all_posts = []
    likes = []

    def __init__(self, filename="botRules.xml"):
        super().__init__(filename)

    def real_perform(self):
        """
            first the two for's to create the users and the posts , the the third one if for likes
        """
        for i in range(self.number_of_users):
            self.users_token.append(self.create_user())
            for p in range(random.randrange(0, self.max_posts_per_user + 1)):
                self.current_user_posts.append(self.create_post(self.users_token[i]))
            self.all_posts += self.current_user_posts
            self.bind_data(self.users_data, self.users_token[i], self.current_user_posts)
        for i in range(len(self.users_token)):
            self.create_likes()

    def create_likes(self):
        start_user = self.find_most_posts_user()
        options_posts_to_like = list(set(self.all_posts) - set(self.users_data[start_user]['posts']))
        self.valid_choices_to_like(options_posts_to_like)
        for p in range(self.max_likes_per_user):
            post_to_like = options_posts_to_like.pop(random.randrange(0, len(options_posts_to_like)))
            self.likes.append(post_to_like)
            self.check_posts_with_zero_likes()
            self.create_post_likes(
                start_user,
                post_to_like
            )

    def find_most_posts_user(self):
        """
            the task demand that the user with the largest amount of posts will start liking
        """
        user_to_return = ""
        last_value = 0
        for user in self.users_token:
            if len(self.users_data[user]['posts']) >= last_value:
                last_value = len(self.users_data[user]['posts'])
                user_to_return = user
        self.users_token.remove(user_to_return)
        return user_to_return

    @staticmethod
    def bind_data(user_dict_data, user_token, post_list):
        user_dict_data[user_token] = {}
        user_dict_data[user_token]['posts'] = post_list[:]
        post_list.clear()

    def create_user(self):
        """
            the extra random field in the username attr is to avoid the unique field at the user model
        """
        data = {
            "username": "TestUserdsa" + str(random.randrange(1, 1000000)),
            "password": "Aa12Aa12",
            "email": "benharushtomer@gmail.com"
        }
        response = requests.post(self.urls['create_user'],
                                 data=data)
        print(response.text)
        return self.get_token(data['username'], data['password'],)

    def get_token(self, username, password):
        post_data = {'username': username, 'password': password}
        r = requests.post(self.urls['get_token'], data=post_data)
        response = json.loads(r.text)
        if "token" in response.keys():
            return response["token"]
        return response["non_field_errors"]

    def create_post(self, token):
        """
            the extra random field in the username attr is to avoid the unique field at the post model
        """
        data = {
            "title": "loren" + str(random.randrange(1, 1000000)),
            "content": "loren2",
        }
        response = requests.post(self.urls['create_post'],
                                 headers={'Authorization': 'Token ' + token},
                                 data=data)
        print(response.text)
        response = json.loads(response.text)
        return response['id']

    def create_post_likes(self, token, post):
        data = {
        "post": post
        }
        response = requests.post(self.urls['create_like'],
                                 headers={'Authorization': 'Token ' + token},
                                 data=data)
        print(response.text)

    def check_posts_with_zero_likes(self):
        """
            one of the task rules is to exit if there is no posts with zero likes
        """
        if not list(set(self.all_posts) - set(self.likes)):
            print("there is no post with 0 likes")
            sys.exit()

    def valid_choices_to_like(self, options_posts_to_like):
        """
            if there is not enough post to like, we cant continue
        """
        if len(options_posts_to_like) < self.max_likes_per_user:
            print("not enough posts to like... change the value at the XML file ")
            sys.exit()

    def __str__(self):
        return "< Bot obj >"
