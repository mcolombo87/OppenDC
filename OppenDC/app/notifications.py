from app.models import Source, Target, SourcesTargets
import requests
from datetime import datetime
from django.core.files.base import ContentFile
from django.conf import settings

def notifyToTargetUpdateReady(target, source_build_version, source_code, url_download, scriptdir):
    url = target.url_target
    headers = {'Content-Type':'application/json'}
    data = {'source_code':source_code, 'version':source_build_version, 'url_download':url_download}
    response = requests.post(url, auth=(target.username, target.password), headers=headers, json=data)
    if response.estatus_code == 200: #OK
        print("NOTIFICACION ENVIADA CON EXITO")#SALVAR COMO UN "NOTIFICADO"
    else:
        print("ERROR, CODIGO: "+ response.status_code)#SALVAR COMO "ERROR" Y GUARDAR RESPUESTA.

def targetsForNotify(update):
    targets = Target.objects.filter(sources_group__code=update.source_code, target_type=update.stage)
    for target in targets:
        notifyToTargetUpdateReady(target, update.source_build_version, update.source_code, update.source_build.url, update.scriptdir_name)