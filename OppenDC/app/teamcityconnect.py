from app.models import Source
import requests
from datetime import datetime

def takeSourcesStatus(sources): #HARDCODEADO, CAMBIAR.
    for s in sources:
        url = 'http://upp.la:8111/app/rest/buildTypes?locator=affectedProject:(id:'+s.code+')&fields=buildType(id,builds($locator(running:false,canceled:false,count:1),build(id,status)))'
        headers = {'Accept':'application/json'}
        response = requests.get(url, auth=('mcolombo', 'aoromi'), headers=headers)
        data = response.json()
        data_status = data['buildType'][0]['builds']['build'][0]['status']
        if data_status == 'SUCCESS':
            data_status = 1
        else: 
            data_status = 0
        s.status = data_status
        s.lastcontrol = datetime.now()
        s.save()
