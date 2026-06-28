from rest_framework import serializers
from .models import Post, Comentario


class PostSerializer(serializers.ModelSerializer):

    autor_nome = serializers.ReadOnlyField(source='autor.usuario.username')

    #Usamos dessa forma acima porque:

    # Quando estamos escrevendo o PostSerializer, nós estamos posicionados dentro da 
    # tabela Post. Cada registro de Post quer olhar para o seu próprio autor e extrair 
    # uma informação de lá.

    # No seu código, a engrenagem roda assim:

    # autor: É o campo que está dentro do model Post. Ele te dá acesso direto à tabela PerfilUsuario.

    # usuario: Dentro da tabela PerfilUsuario, você criou o campo 
    # usuario = models.OneToOneField(User...). Então, através do perfil, você consegue 
    # acessar a tabela User nativa do Django.

    # username: É o atributo de texto real que guarda o nome de usuário (ex: nicolas_ramos) 
    # dentro da tabela User.

    # Por isso, o caminho autor.usuario.username é um caminho direto e linear "para cima" (
    # da tabela filha para a tabela pai).


    # Com isso, não é autor.posts.nome porque


    # Inversão de Fluxo (posts): O related_name='posts' que você definiu 
    # no model serve para a tabela PerfilUsuario olhar "para baixo" e descobrir quais 
    # posts pertencem a ela. Como você já está dentro de um Post específico, tentar acessar 
    # .posts confunde o Django, pois você estaria tentando buscar todos os posts desse autor 
    # em vez dos dados do próprio autor.

    class Meta:
        model = Post
        fields = ['id', 'titulo', 'descricao', "conteudo", 'criado_em', 'autor_nome']


class ComentarioSerializer(serializers.ModelSerializer):
    autor_nome = serializers.ReadOnlyField(source='autor.usuario.username')
    post_titulo = serializers.ReadOnlyField(source='post.titulo')

    class Meta:
        model = Comentario
        fields = ['id', 'autor_nome', 'post_titulo', 'conteudo', 'criado_em']
