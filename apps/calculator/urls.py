from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('calculator/', calculator_page, name='calculator'),
    path('novo-registro/', novo_registro, name='novo-registro'),
    path('limpar-registros/', limpar_registros, name='limpar-registros'),
]