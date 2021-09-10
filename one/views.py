from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import requests
from django.http import HttpResponse

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "GET":
        return redirect('/')
    
    errors = User.objects.validate(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered")
        return redirect('/main')
        
    
    
def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in")
    return redirect('/main')
    
    
def logout(request):
    request.session.clear()
    return redirect('/')

def main(request):
    return render(request, "main.html")

def data(request):
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    
    info = requests.get(url).json()

    context = {'info': info}

    return render(request, 'data.html', context)
