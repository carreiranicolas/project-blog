from rest_framework import viewsets
from .models import Comentario, Post, PerfilUsuario
from .serializers import ComentarioSerializer, PostSerializer


# Create your views here.

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


