from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_page, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('logout/', logout_user, name='logout'),
]