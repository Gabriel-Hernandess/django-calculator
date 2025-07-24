from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
import json

from ..core.decorators.decorators import login_required_custom
from .models import Usuario
from ..users.models import Operacao

class Index_View(View):
    def get(self, request):
        return render(request, 'index.html')

@method_decorator(login_required_custom, name='dispatch')
class Calculator_View(View):
    def get(self, request):
        usuario_id = request.session.get('usuario_id')

        try:
            user = Usuario.objects.get(IDUsuario=usuario_id)
        except Usuario.DoesNotExist:
            return redirect('login')

        operacoes_qs = Operacao.objects.filter(Usuario=user).order_by('-DtInclusao')
        operacoes = list(operacoes_qs.values('Parametros', 'Resultado', 'DtInclusao'))

        return render(request, 'calculator.html', {'operacoes': operacoes})

@method_decorator(login_required_custom, name='dispatch')
class Novo_registro(View):
    def post(self, request):
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
    
    def get(self, request):
        return JsonResponse({'error': 'Método não permitido'}, status=405)

@method_decorator(login_required_custom, name='dispatch')
class Limpar_Registros(View):
    def post(self, request):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return JsonResponse({'error': 'Usuário não autenticado'}, status=401)

        Operacao.objects.filter(Usuario_id=usuario_id).delete()
        return JsonResponse({'success': True})

    def get(self, request):
        return JsonResponse({'error': 'Método não permitido'}, status=405)