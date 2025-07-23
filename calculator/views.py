from django.shortcuts import render
from django.http import HttpResponse

def login_page(request):
    if request.method == 'GET':
        return render(request, 'login.html', status=200)

def calculator_page(request):
    return HttpResponse('TELA DA CALCULADORA')