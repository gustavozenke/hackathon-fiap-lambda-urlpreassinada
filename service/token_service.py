import os

import jwt


class TokenService:

    def __init__(self):
        self.__secret = os.getenv('secret')
        self.__algorithm = os.getenv('algorithm')

    def encode_jwt_token(self, event):
        return jwt.encode(event, self.__secret, self.__algorithm)

    def decode_jwt_token(self, token):
        jwt.decode(token, self.__secret, self.__algorithm)
