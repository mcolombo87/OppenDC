from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from app.models import Source, Update
from app import teamcityconnect, notifications
from datetime import datetime, timedelta

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('OppenDC')
    return render(request, 'app/index.html')

def loginPage(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['inputUsername']
            password = request.POST['inputPassword']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                # context = {'username': user.username }
                return HttpResponseRedirect(reverse('OppenDC'))
            else:   
                return render(request, 'app/login.html', {'retry':True})
        else: return render(request, 'app/login.html')
    else: return HttpResponseRedirect(reverse('OppenDC'))

@login_required()
def home(request):
    user = request.user
    last_name = user.last_name
    first_name = user.first_name
    if len(first_name) > 0 and len(last_name) > 0:
        name_to_show = user.last_name +', '+ user.first_name
    else:
        name_to_show = user.username
    request.session['name_to_show'] = name_to_show
    sources = Source.objects.all()
    if 'refresh_sources' in request.POST:
        teamcityconnect.takeSourcesStatus(sources)
    context = {'sources': sources } #sources[0].name
    return render(request, 'app/home.html', context)

@login_required()
def deploy(request):
    if request.method == 'POST':
        if 'candidate' in request.POST:
            source_candidate = Source.objects.get(id=request.POST['candidate'])
            record = Update(source_code=source_candidate.code)
            record.create_datetime = datetime.now()
            record.source_build_version = source_candidate.build_version
            record.stage = 0 #QA UPDATE_STATOS, see models.
            record.closed = False
            record.next_stage_datetime_set = datetime.now() + timedelta(days=1)
            record.internal_teamcity_build = source_candidate.internal_teamcity_build
            file_name = str(source_candidate.code)+"V"+str(source_candidate.build_version)+".zip"
            record.source_build.save(file_name, teamcityconnect.takeSourceBuild(record))
            record.save()
            print("ENTRE EN CANDIDATO")
        if 'deploy' in request.POST:
            print('ENTRE EN DEPLOY')
            update = Update.objects.get(id=request.POST['deploy'])
            notifications.targetsForNotify(update)

    deploys = Update.objects.all()
    context = {'deploys': deploys }
    return render(request, 'app/deploy.html', context)