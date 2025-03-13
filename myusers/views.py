from django.shortcuts import redirect, render
from myusers.forms import LoginForm
from django.contrib.auth.models import User
from django.contrib import auth, messages

def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form['username'].value()
            password = form['password'].value()

        usuario = auth.authenticate(
            request,
            username=username, 
            password=password)
        
        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, f'{username.upper()} logado com sucesso')
            return redirect('index')
        else:
            messages.error(request, 'Erro ao efetuar login.')
            return redirect('login')
    return render(request, 'myusers/login.html',{"form":form})

def logout(request):
    auth.logout(request)
    return redirect('login')