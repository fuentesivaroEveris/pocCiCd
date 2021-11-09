import requests
import json
import sys
import os

def mainValid(major,minor,version,environment,groupid,nameraml):
    nameApplication = getTitle()
    print(nameApplication)
    responsePublishDesign = ''
    tokenAuth = loginValid()
    responseExistAsset = validExistAsset(tokenAuth,nameApplication)
    #if responseExistAsset == 'no':
    #    return 'valid ok'
    responseCreateAsset = publishAsset(tokenAuth,major,minor,version,nameApplication,groupid,environment,nameraml)
    #    responsePublishDesign = publishAsset()
    #response = publishAsset(tokenAuth,major,minor,version)
    responseoldApiManager = oldPublishApiManager(tokenAuth,nameApplication,groupid,environment)
    print(responseExistAsset)
    print(responseoldApiManager)
    
    for item in responseoldApiManager:
        print(deleteApiManager(tokenAuth,item))
        
        
    responseApiManager = publishApiManager(tokenAuth,major,minor,version,nameApplication)
    print(responseApiManager)
        
    return 'ok'

def getTitle():
    with open('api-cicd-examplewho-poc.raml') as f:
        lines = f.readlines()
        for ii in lines:
            x = ii.find("title:")
            if x >= 0:
                ii = ii.replace(' ','')
                ii = ii.replace('title:','')
                ii = ii.replace('\n', ' ').replace('\r', '')
                ii = ii.strip()
                return ii
    return 1
    
def loginValid():
    url = "https://eu1.anypoint.mulesoft.com//accounts/login"
    payload='username=jtorpoco&password=Maniac321.'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    responseObj = json.loads(response.text)
    token = responseObj['access_token']
    return token

def validExistAsset(tokenAuth,name):
    url = "https://eu1.anypoint.mulesoft.com//exchange/api/v1/assets?search="+ name
    payload={}
    headers = {
      'Authorization': 'Bearer ' + tokenAuth,
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    ss = response.text
    if '[]' == ss:
        return 'no'
    return 'si'


def publishAsset(tokenAuth,major,minor,version,name,groupid,environment,nameraml):
    url = "https://eu1.anypoint.mulesoft.com//apimanager/api/v1/organizations/"+groupid+"/environments/"+environment+"/apis"
    major = str(major)
    minor = str(minor)
    version = str(version)
    print(name)
    name = name.replace('\n', ' ').replace('\r', '')
    name = name.strip()
    url = "https://eu1.anypoint.mulesoft.com//exchange/api/v1/assets"
    payload={'organizationId': groupid,
    'groupId': groupid,
    'assetId': name,
    'version': major+"."+minor+"."+version,
    'name': name,
    'classifier': 'raml',
    'apiVersion': 'v1'}
    files=[
      ('asset',(nameraml,open(nameraml,'rb'),'application/octet-stream'))
    ]
    headers = {
      'Authorization': 'Bearer ' + tokenAuth,
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    if(response.status_code=='200'):
        return 'ok'
    return response.status_code

def oldPublishApiManager(tokenAuth,name,groupid,environment):
    url = "https://eu1.anypoint.mulesoft.com//apimanager/api/v1/organizations/"+groupid+"/environments/"+environment+"/apis?ascending=false&limit=20&offset=0&sort=createdDate"
    payload={}
    headers = {
      'Authorization': 'Bearer ' + tokenAuth,
    }
    
    listApis=[]

    
    
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.text
    dataDict = json.loads(data)
    for item in dataDict['assets']:
        if item['assetId'] == name:
            for item2 in item['apis']:
                if item2['assetId'] == name:
                    print(item2['id'])
                    listApis.append(item2['id'])

    
    #data = json.load(response.text)
    #for item in data:
    #    print(item)
    #return 'ok'
    #return response.text
    return listApis

def publishApiManager(tokenAuth,major,minor,version,name):
    major = str(major)
    minor = str(minor)
    version = str(version)
    print(name)
    name = name.replace('\n', ' ').replace('\r', '')
    name = name.strip()
    url = "https://eu1.anypoint.mulesoft.com//apimanager/api/v1/organizations/3f50a308-b636-4db8-84be-c62ad0c4dd31/environments/459a61e1-f4ca-4acf-a6ad-bfa8e2548b7b/apis"
    payload = json.dumps({
        "endpoint": {
        "deploymentType": "CH",
        "isCloudHub": None,
        "muleVersion4OrAbove": None,
        "proxyUri": None,
        "referencesUserDomain": None,
        "responseTimeout": None,
        "type": "raml",
        "uri": None
      },
      "providerId": None,
      "instanceLabel": None,
      "spec": {
        "assetId": name,
        "groupId": "3f50a308-b636-4db8-84be-c62ad0c4dd31",
        "version": major+"."+minor+"."+version
      }
    })
    print(payload)

    headers = {
        'Authorization': 'Bearer ' + tokenAuth,
        'Content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)    
    print(response.text)
    if(response.status_code=='200'):
        return 'ok'
    return response.status_code



def deleteApiManager(tokenAuth,apiid):
    url = "https://eu1.anypoint.mulesoft.com//apimanager/api/v1/organizations/3f50a308-b636-4db8-84be-c62ad0c4dd31/environments/459a61e1-f4ca-4acf-a6ad-bfa8e2548b7b/apis/"+ str(apiid)

    headers = {
            'Authorization': 'Bearer 2bef8037-f35d-4a32-8fa1-9b2f190eec5b',
    }
    
    response = requests.request("DELETE", url, headers=headers, data=payload)

    return response.text

