from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from .decorators import login_required_custom
from django.contrib import messages
from django.db import IntegrityError

from django.http import HttpResponse
from .models import Usuario

def login_page(request):
    if request.method == 'GET':
        return render(request, 'login.html', status=200)
    
    elif request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        print(email, senha)
        print(Usuario.objects.all())

        try:
            user = Usuario.objects.get(Email=email, Senha=senha)
            
            request.session['usuario_id'] = user.IDUsuario
            request.session['usuario_nome'] = user.Nome

            return redirect('calculator')
        except Usuario.DoesNotExist:
            msg = 'Usuário ou senha inválidos'
            return render(request, 'login.html', {'msg': 'Email ou senha incorreto'})
        
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if Usuario.objects.filter(Email=email).exists():
            return HttpResponse('USUÁRIO JÁ CADASTRADO')

        try:
            Usuario.objects.create(Nome=nome, Email=email, Senha=senha)
            user = Usuario.objects.get(Email=email, Senha=senha)

            request.session['usuario_id'] = user.IDUsuario
            request.session['usuario_nome'] = user.Nome

            return redirect('/calculator/')
        except IntegrityError:
            messages.error(request, 'Email já cadastrado.')

@login_required_custom
def logout_user(request):
    request.session.flush()
    return redirect('login')

@login_required_custom
def calculator_page(request):
    return render(request, 'calculator.html')