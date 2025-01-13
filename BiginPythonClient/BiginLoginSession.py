
from PythonAPIClientBase import LoginSession
import requests
import json

#Scopes list: https://www.bigin.com/developer/docs/apis/v2/scopes.html

class BiginLoginSession(LoginSession):
    loggedin = None
    endpoint = None
    access_token = None
    refresh_token = None
    scope = None
    api_domain = None
    token_type = None
    expires_in = None

    def __init__(self, endpoint):
        self.loggedin = False
        self.endpoint = endpoint

    def register_auth_code(self, auth_code):
        raise Exception("Not overriddern")

    def _get_api_url(self, path):
        return "https://accounts." + self.endpoint + path


class ServerBasedBiginLoginSession(BiginLoginSession):
    client_id = None
    client_secret = None
    redirect_url = None
    scopes = None
    def __init__(self, client_id, client_secret, endpoint, redirect_url, scopes):
        super().__init__(endpoint)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url
        self.scopes = scopes


    def get_auth_url(self):
        offline_access = True
        access_type = "online"
        if offline_access:
            access_type = "offline"
        apipath = "/oauth/v2/auth?scope=" + self.scopes \
            + "&client_id=" + self.client_id \
            + "&response_type=code" \
            + "&access_type=" + access_type \
            + "&redirect_uri=" + self.redirect_url
        return self._get_api_url(apipath)

    def register_auth_code(self, auth_code):
        ##"https://accounts.zoho.com/oauth/v2/token"
        url = self._get_api_url("/oauth/v2/token")
        headers={
            "Accept": "application/json"
        }
        post_form_data = {
            "client_id": (None, self.client_id),
            "client_secret": (None, self.client_secret),
            "code": (None, auth_code),
            "redirect_uri": (None, self.redirect_url),
            "grant_type": (None, "authorization_code")
        }
        print("DDD", post_form_data)

        response = requests.post(url, headers=headers, files=post_form_data)
        if response.status_code != 200:
            print("Error")
            print("Got response status", response.status_code)
            print("Response text", response.text)
            raise Exception("Invalid Auth")
        responseDict = json.loads(response.text)
        if "error" in responseDict:
            print("Error -", responseDict["error"])
            print("Got response status", response.status_code)
            print("Response text", response.text)
            raise Exception("Invalid Auth")

        print("Valid response")
        print("Response text", response.text)

class SelfBasedBiginLoginSession(BiginLoginSession):
    client_id = None
    client_secret = None
    endpoint = None
    def __init__(self, client_id, client_secret, endpoint):
        super().__init__(endpoint)
        self.client_id = client_id
        self.client_secret = client_secret

    # https://api-console.zoho.eu/

    def register_auth_code(self, auth_code):
        ##"https://accounts.zoho.com/oauth/v2/token"
        url = self._get_api_url("/oauth/v2/token")
        headers={
            "Accept": "application/json"
        }
        post_form_data = {
            "client_id": (None, self.client_id),
            "client_secret": (None, self.client_secret),
            "code": (None, auth_code),
            "grant_type": (None, "authorization_code")
        }
        print("URL", url)
        print("Form Data", post_form_data)

        response = requests.post(url, headers=headers, files=post_form_data)
        if response.status_code != 200:
            print("Error")
            print("Got response status", response.status_code)
            print("Response text", response.text)
            raise Exception("Invalid Auth")
        responseDict = json.loads(response.text)
        if "error" in responseDict:
            print("Error -", responseDict["error"])
            print("Got response status", response.status_code)
            print("Response text", response.text)
            raise Exception("Invalid Auth")

        self.loggedin = True
        access_token = None
        refresh_token = None
        scope = None
        api_domain = None
        token_type = None
        expires_in = None

        print("Valid response")
        print("Response text", response.text)
