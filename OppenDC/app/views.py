from django.shortcuts import render, redirect,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from django.template import RequestContext

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
    context = {'username':'PRUEBA'}
    return render(request, 'app/navigationBarHead.html', context)

    