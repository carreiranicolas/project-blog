from django.urls import path, include
from rest_framework.routers import DefaultRouter
from.views import ComentarioViewSet, PostViewSet

# O Router cria as rotas de listagem e detalhe automaticamente para nós

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comentarios', ComentarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
