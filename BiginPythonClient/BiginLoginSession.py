
from PythonAPIClientBase import LoginSession
import requests

class BiginLoginSession(LoginSession):
    pass

class ServerBasedBiginLoginSession(BiginLoginSession):
    client_id = None
    client_secret = None
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

