from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')

    telefone = models.CharField(
        max_length=11,
        blank=True,
        default=''
    )

    data_nascimento = models.DateField(
        null=False,
        blank=False
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        return f'{self.usuario}'

class Post(models.Model):

    autor = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='posts')

    titulo = models.CharField(
        max_length=120,
        null=False,
        blank=False
    )

    descricao = models.TextField()

    criado_em = models.DateTimeField(auto_now_add=True)

    atualizado_em = models.DateTimeField(auto_now=True)

    oculto = models.BooleanField(
        default=False
    )

    excluido = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f'{self.autor} - ({self.pk}) {self.titulo}'



class Comentario(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='comentarios')
    conteudo = models.TextField()
    excluido = models.BooleanField(
        default=False
    )
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f'{self.atualizado_em} - {self.autor}'

