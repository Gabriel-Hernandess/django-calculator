from django.urls import path
from .views import Login_View, Register_View, Logout_User

urlpatterns = [
    path('login/', Login_View.as_view(), name='login'),
    path('cadastro/', Register_View.as_view(), name='cadastro'),
    path('logout/', Logout_User.as_view(), name='logout'),
]