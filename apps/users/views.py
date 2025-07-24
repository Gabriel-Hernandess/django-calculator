from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError

from ..core.decorators.decorators import *
from .models import Usuario

# Create your views here.
def login_page(request):
    if request.method == 'GET':
        if request.session.get('usuario_id'):
            return redirect('calculator')
        return render(request, 'login.html', status=200)
    
    elif request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            user = Usuario.objects.get(Email=email, Senha=senha)
            
            request.session['usuario_id'] = user.IDUsuario
            request.session['usuario_nome'] = user.Nome

            return redirect('calculator')
        except Usuario.DoesNotExist:
            return render(request, 'login.html', {'msg': 'Confira os dados e tente novamente.'})
        
def cadastro(request):
    if request.method == 'GET':
        if request.session.get('usuario_id'):
            return redirect('calculator')
        return render(request, 'cadastro.html')
    
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not all([nome, email, senha]):
            return render(request, 'cadastro.html', {'msg': 'Confira os dados e tente novamente.'})

        if Usuario.objects.filter(Email=email).exists():
            return render(request, 'cadastro.html', {'msg': 'Email já está em uso.'})

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