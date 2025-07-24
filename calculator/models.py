from django.db import models

class Usuario(models.Model):
    IDUsuario = models.AutoField(primary_key=True)
    Nome = models.CharField(max_length=255, null=False)
    Email = models.EmailField(unique=True, null=False)
    Senha = models.CharField(max_length=255, null=False)
    DtInclusao = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.Email


class Operacao(models.Model):
    IDOperacao = models.AutoField(primary_key=True)
    
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='IDUsuario')

    Parametros = models.CharField(max_length=255, null=False)
    Resultado = models.CharField(max_length=255, null=False)
    DtInclusao = models.DateField(auto_now=True)

    def __str__(self):
        return f"Operação #{self.IDOperacao}"