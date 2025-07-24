from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from .decorators import login_required_custom
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
import json

from django.http import HttpResponse
from .models import Usuario, Operacao

def login_page(request):
    if request.method == 'GET':
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
    if request.method == 'GET':
        usuario_id = request.session.get('usuario_id')

        try:
            user = Usuario.objects.get(IDUsuario=usuario_id)
        except Usuario.DoesNotExist:
            return redirect('login')

        operacoes_qs = Operacao.objects.filter(Usuario=user).order_by('-DtInclusao')
        operacoes = list(operacoes_qs.values('Parametros', 'Resultado', 'DtInclusao'))

        return render(request, 'calculator.html', {'operacoes': operacoes})

@login_required_custom
def novo_registro(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            print(data)

            usuario_id = data.get('usuarioId')
            if not usuario_id:
                return JsonResponse({'error': 'Usuário não informado'}, status=400)
            
            try:
                usuario = Usuario.objects.get(pk=usuario_id)
            except Usuario.DoesNotExist:
                return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
            
            Operacao.objects.create(
                Usuario=usuario,
                Parametros=data['expressao'],
                Resultado=data['resultado']
            )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required_custom
def limpar_registros(request):
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return JsonResponse({'error': 'Usuário não autenticado'}, status=401)

        Operacao.objects.filter(Usuario_id=usuario_id).delete()
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Método não permitido'}, status=405)