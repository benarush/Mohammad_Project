import requests
import json

"""
    I know that there is a module of hunter.io that i can use more easily, but to reduce dependencies
    for this test i use my own API obj
"""


class Config:
    hunter_pk = "d4f5f63afc56481d208f6b5efde092128219db95"


class API(Config):

    def __init__(self, email):
        self.email = email

    def hunter_validation(self):
        self.get_hunter_data()
        return self.is_valid_email()

    def get_hunter_data(self):
        get_params = {"email": self.email, "api_key": self.hunter_pk}
        response = requests.get("https://api.hunter.io/v2/email-verifier", params=get_params)
        self.hunter_api_response = json.loads(response.text)

    def is_valid_email(self):
        status = self.hunter_api_response["data"]["status"]
        return status == "webmail" or status == "valid"
