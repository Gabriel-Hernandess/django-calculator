from django.urls import path

from .views import Index_View, Calculator_View, Novo_registro, Limpar_Registros

urlpatterns = [
    path('', Index_View.as_view(), name='home'),
    path('calculator/', Calculator_View.as_view(), name='calculator'),
    path('novo-registro/', Novo_registro.as_view(), name='novo-registro'),
    path('limpar-registros/', Limpar_Registros.as_view(), name='limpar-registros'),
]