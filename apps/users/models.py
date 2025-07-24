from django.db import models
from ..calculator.models import Usuario

# Create your models here.
class Operacao(models.Model):
    IDOperacao = models.AutoField(primary_key=True)
    
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='IDUsuario')

    Parametros = models.CharField(max_length=255, null=False)
    Resultado = models.CharField(max_length=255, null=False)
    DtInclusao = models.DateField(auto_now=True)

    def __str__(self):
        return f"Operação #{self.IDOperacao}"