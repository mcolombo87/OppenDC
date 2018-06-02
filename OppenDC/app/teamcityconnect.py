from app.models import Source
import requests
from datetime import datetime
from django.core.files.base import ContentFile
from django.conf import settings

def takeSourcesStatus(sources):
    for s in sources:
        url = settings.TC_BASE_URL+'buildTypes?locator=affectedProject:(id:'+s.code+')&fields=buildType(id,builds($locator(running:false,canceled:false,count:1),build(id,status,number)))'
        headers = {'Accept':'application/json'}
        response = requests.get(url, auth=(settings.TC_USERNAME, settings.TC_PASSWORD), headers=headers)
        data = response.json()
        data_status = data['buildType'][0]['builds']['build'][0]['status']
        data_build_version = data['buildType'][0]['builds']['build'][0]['number']
        data_internal_teamcity_buid = data['buildType'][0]['builds']['build'][0]['id']
        if data_status == 'SUCCESS':
            data_status = 1
        else: 
            data_status = 0
        s.status = data_status
        s.lastcontrol = datetime.now()
        s.build_version = data_build_version
        s.internal_teamcity_build = data_internal_teamcity_buid
        s.save()

def takeSourceBuild(update_record):
    url = settings.TC_BASE_URL+'builds/id:'+str(update_record.internal_teamcity_build)+'/artifacts/content/'+update_record.source_code+'.zip'
    headers = {'Media-Type':'application/zip'}
    response = requests.get(url, auth =(settings.TC_USERNAME, settings.TC_PASSWORD), headers=headers)
    f = ContentFile(response.content)
    return  f 