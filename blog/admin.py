from django.contrib import admin
from .models import Comentario, Post, PerfilUsuario

# Register your models here.

admin.site.register(PerfilUsuario)
admin.site.register(Comentario)
admin.site.register(Post)
