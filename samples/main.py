# Simple Sample
import sys
sys.path.append('../')
import BiginPythonClient
import json
from InquirerPy import inquirer


print("Start of simple test")


#print("DD", secrets)

def getServerBasedLogin(bigin_client):
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

def getClientBasedLogin(bigin_client):
    secret_file = "../secrets/self_client_secrets.json"
    token_file = "../secrets/self_client_secrets_token.json"
    secrets = None
    with open(secret_file) as json_data:
        secrets = json.load(json_data)
    login_session = bigin_client.getSelfBasedBiginLoginSessionInteractive(
        client_id=secrets["client_id"],
        client_secret=secrets["client_secret"],
        endpoint=secrets["endpoint"],
        token_file=token_file,
        inquirer=inquirer
    )
    return login_session

bigin_client = BiginPythonClient.BiginClient()
login_session = getClientBasedLogin(bigin_client)

pipelines = bigin_client.getLayouts(loginSession=login_session, module=BiginPythonClient.Module.PIPELINES)

deal_sourcers_meet_pipeline = pipelines.getPipeline(name="Deal Sourcers meet")

if deal_sourcers_meet_pipeline is None:
    print("Pipeline not found")
    exit(0)

# fields = deal_sourcers_meet_pipeline.getFields()
# for field in fields.items:
#     print(field.dict["api_name"])  #Contact_Name

field_api_names = "Contact_Name,Stage"

contacts = deal_sourcers_meet_pipeline.getRecords(fields=field_api_names)

wahted_stage = "Contacted next day"

filtered_contacts = []
for contact in contacts:
    if contact["Stage"] == wahted_stage:
        filtered_contacts.append(contact)

for contact in filtered_contacts:
    print(contact)

#
# stages = deal_sourcers_meet_pipeline.getStages()
#
# for stage in stages:
#     print(stage)


print("End of simple test")
