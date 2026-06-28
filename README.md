🧱 A Estrutura do Banco (Models)
Não mude muito além disso no começo para não perder o foco do DRF:

Post: Título, Conteúdo, Data de Publicação, Status (Rascunho/Publicado) e Autor (conectado ao usuário do Django).

Comentario: Post (FK), Nome do Autor, Conteúdo e Data.

🚀 O que você vai dominar no DRF com esse projeto
Fazer um blog vai te forçar a sair do básico (CRUD puro) e implementar regras de negócio reais usando as ferramentas nativas do framework:

Autenticação e Permissões (Permissions):

O desafio: Qualquer pessoa pode ler os posts (GET), mas apenas usuários autenticados podem criar posts (POST). Além disso, um usuário só pode editar ou deletar (PUT/DELETE) o seu próprio post.

O que você usa: IsAuthenticatedOrReadOnly e uma permissão customizada baseada em BasePermission.

Serializers Customizados:

O desafio: Quando alguém listar os posts, você não quer que apareça apenas o id do autor, mas sim o username dele.

O que você usa: SlugRelatedField ou ReadOnlyField(source='autor.username').

Filtros e Buscas (Filtering):

O desafio: Permitir que o usuário busque posts por título ou filtre apenas os que estão com o status "Publicado".

O que você usa: filters.SearchFilter nativo do DRF.

Paginação (Pagination):

O desafio: Um blog de verdade não entrega 500 posts de uma vez no JSON.

O que você usa: Configurar a paginação padrão no settings.py para entregar, por exemplo, 10 posts por página.
