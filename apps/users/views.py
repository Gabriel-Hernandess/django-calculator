from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db import IntegrityError

from ..core.decorators.decorators import *
from .models import Usuario

# Create your views here.
class Login_View(View):
    def get(self, request):
        if request.session.get('usuario_id'):
            return redirect('calculator')
        return render(request, 'login.html', status=200)
    
    def post(self, request):
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            user = Usuario.objects.get(Email=email, Senha=senha)
            
            request.session['usuario_id'] = user.IDUsuario
            request.session['usuario_nome'] = user.Nome

            return redirect('calculator')
        except Usuario.DoesNotExist:
            return render(request, 'login.html', {'msg': 'Confira os dados e tente novamente.'})
        
class Register_View(View):
    def get(self, request):
        if request.session.get('usuario_id'):
            return redirect('calculator')
        return render(request, 'cadastro.html')
    
    def post(self, request):
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

method_decorator(login_required_custom, name='dispatch')
class Logout_User(View):
    def post(self, request):
        request.session.flush()
        return redirect('login')