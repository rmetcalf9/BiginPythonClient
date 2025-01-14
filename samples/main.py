# Simple Sample
import sys
sys.path.append('../')
import BiginPythonClient
import json
from InquirerPy import inquirer


print("Start of simple test")


#print("DD", secrets)

def getServerBasedLogin():
    secret_file = "../secrets/client_secrets.json"
    secrets = None
    with open(secret_file) as json_data:
        secrets = json.load(json_data)
    login_session = BiginPythonClient.ServerBasedBiginLoginSession(
        client_id=secrets["client_id"],
        client_secret=secrets["client_secret"],
        endpoint=secrets["endpoint"],
        redirect_url=secrets["redirect_url"],
        scopes=secrets["scopes"]
    )
    print("Visit this site", login_session.get_auth_url())
    return login_session

def getClientBasedLogin():
    secret_file = "../secrets/self_client_secrets.json"
    token_file = "../secrets/self_client_secrets_token.json"
    secrets = None
    with open(secret_file) as json_data:
        secrets = json.load(json_data)
    login_session = BiginPythonClient.SelfBasedBiginLoginSessionInteractive(
        client_id=secrets["client_id"],
        client_secret=secrets["client_secret"],
        endpoint=secrets["endpoint"],
        token_file=token_file,
        inquirer=inquirer
    )
    return login_session

login_session = getClientBasedLogin()


print("End of simple test")
