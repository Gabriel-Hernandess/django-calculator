from django.db import models

class Usuario(models.Model):
    IDUsuario = models.AutoField(primary_key=True)
    Nome = models.CharField(max_length=255, null=False)
    Email = models.EmailField(unique=True, null=False)
    Senha = models.CharField(max_length=255, null=False)
    DtInclusao = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.Email