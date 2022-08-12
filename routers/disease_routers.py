from fastapi import APIRouter
import requests

from config.config import settings

router = APIRouter()


@router.get("/who-entity/{id}")
async def get_diseases(id: str):

    token_endpoint = 'https://icdaccessmanagement.who.int/connect/token'
    client_id = settings.icd_client_id
    client_secret = settings.icd_client_Secret
    scope = 'icdapi_access'
    grant_type = 'client_credentials'


    # get the OAUTH2 token

    # set data to post
    payload = {'client_id': client_id, 
            'client_secret': client_secret, 
            'scope': scope, 
            'grant_type': grant_type}
            
    # make request
    r = requests.post(token_endpoint, data=payload, verify=False).json()
    token = r['access_token']


    # access ICD API

    #id_entity = id
    id_entity = '257068234'
    uri = 'https://id.who.int/icd/entity/' + id_entity

    # HTTP header fields to set
    headers = {
        'Authorization':  'Bearer '+ token, 
        'Accept': 'application/json', 
        'Accept-Language': 'es',
        'API-Version': 'v2'
    }
            
    # make request           
    r = requests.get(uri, headers=headers, verify=False)

    # print the result
    print (r.text)

    return r.text