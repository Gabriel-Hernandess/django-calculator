from django.urls import path
from .views import *

urlpatterns = [
    path('calculator/', calculator_page, name='calculator'),
    path('novo-registro/', novo_registro, name='novo-registro'),
    path('limpar-registros/', limpar_registros, name='limpar_registros'),

    path('login/', login_page, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('logout/', logout_user, name='logout'),
]