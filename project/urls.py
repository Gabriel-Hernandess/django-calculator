from django.urls import path, include

urlpatterns = [
    path('', include('apps.calculator.urls')),
    path('', include('apps.users.urls')),
]