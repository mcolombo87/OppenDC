from django.shortcuts import render, redirect,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from app.models import Source
from app import teamcityconnect

def index(request):
    if request.user.is_authenticated:
        logout(request) # LOGOUT DE PRUEBA, BORRAR LUEGO.
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
    sources = Source.objects.all()
    if 'refresh_sources' in request.POST:
        teamcityconnect.takeSourcesStatus(sources)
    context = {'username':name_to_show, 'sources': sources } #sources[0].name
    return render(request, 'app/home.html', context)

    