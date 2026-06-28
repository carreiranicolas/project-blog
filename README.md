# 📖 Projeto Blog - Guia de Construção e Integração (Full Stack)

Este documento registra o passo a passo técnico utilizado para a construção da API Rest com Django Rest Framework (DRF) e sua integração com o front-end em React (Vite).

---

## 🐍 Etapa 1: Configuração e Blindagem do Backend (Django)

### 1. Instalação das Dependências Core
Criação do ambiente virtual e instalação dos pacotes necessários para transformar o Django em uma API que aceita requisições externas e gerencia variáveis de ambiente de forma segura:
```bash
python -m venv .venv

source .venv/bin/activate # Linux e Mac

pip install djangorestframework django-cors-headers python-dotenv
```

### 2. Segurança e Varíaveis ambientes

```text
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```


No settings.py:

```bash

from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

INSTALLED_APPS = [
    # ... apps padrão do django
    'rest_framework',
    'corsheaders',
    'blog',  # App local do ecossistema do Blog
]


```

### 3: Configuração do Middleware do CORS

Para que o Django intercepte as requisições e adicione os cabeçalhos de permissão antes de enviar as respostas, adicionamos o CorsMiddleware no topo da lista de MIDDLEWARE:

```bash

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Deve ficar o mais alto possível
    'django.middleware.common.CommonMiddleware',
    # ... outros middlewares
]

```

### 4. Liberação de origens permitadas (CORS):

Configuração dos domínios e portas de desenvolvimento do React (tanto o padrão do antigo Create React App quanto o do Vite) autorizados a consumir esta API:

```bash

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "[http://127.0.0.1:3000](http://127.0.0.1:3000)",
    "http://localhost:5173",  # Porta padrão do Vite
    "[http://127.0.0.1:5173](http://127.0.0.1:5173)",
]

```


## 🏗️ Etapa 2: O Fluxo de Dados na API (MVT para REST)

Com a infraestrutura pronta, o desenvolvimento seguiu o fluxo padrão do DRF para expor os endpoints:

```text
[Banco de Dados] ──> [Models] ──> [Serializers (JSON)] ──> [ViewSets] ──> [Routers (URLs)]

```

### 5. Models

(models.py): Modelagem das tabelas do banco de dados relacional (PerfilUsuario, Post, Comentario) utilizando o ORM nativo do Django.

### 6. Serializers

Serializers (serializers.py): Criação das classes que herdam de serializers.ModelSerializer. O papel deles é traduzir as instâncias dos models do Python para o formato JSON (saída) e validar os dados recebidos do front-end (entrada).


### 7. Views

(views.py): Implementação utilizando viewsets.ModelViewSet. Em vez de escrever métodos manuais para GET, POST, PUT e DELETE, a ViewSet amarra o queryset (dados do banco) ao seu serializer_class específico, gerando todo o CRUD automaticamente.


### 8. Roteamento

(urls.py): Acoplamento das ViewSets utilizando o DefaultRouter do DRF. O router analisa a ViewSet e gera automaticamente caminhos limpos como /posts/ e /posts/<id>/.


## ⚛️ Etapa 3: Inicialização e Conexão do Frontend (React)

### 9. Criação do Projeto com Vite

Utilização do Vite para criar uma estrutura SPA (Single Page Application) leve e veloz, especificando a versão compatível com o ambiente Node local:

```text
npx create-vite@5.0.0 frontend --template react

#fizemos isso para eliminar um problema logo de cara, mas o certo é:


```

### 10. Instalação de Dependências do Front


```text
cd frontend
npm install
npm install axios
```


### 11. Arquitetura do Cliente de API (src/services/api.js)

```bash
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/', // URL base do backend Django
});

export default api;
```

### 12. Execução do Ambiente de Desenvolvimento

Para testar e validar o consumo dos dados em tempo real utilizando os hooks useState e useEffect, subimos o servidor de desenvolvimento do Vite:

```bash
npm run dev

```

## Etapa 4: Autenticação com JWT

🔑 Como funciona o fluxo com JWT?

1. O usuário se cadastra e faz login em uma tela do React.

2. O Django valida as credenciais e devolve um "Token" (uma string criptografada super longa).

3. O React guarda esse token.

4. Toda vez que o usuário tentar criar um post ou comentar, o React envia esse token no cabeçalho (Header) da requisição Axios.

5. O Django lê o token, reconhece o usuário e autoriza a ação. Se um usuário anônimo tentar fazer o mesmo, o Django barra com um HTTP 401 Unauthorized.


🛠️ O Plano de Ação no Backend
Para implementar isso de forma limpa, nós usamos o pacote django-rest-framework-simplejwt, que faz todo o trabalho pesado de criptografia e gerenciamento de tokens para nós.

Os passos no Django seriam:

### 1.Instalar pacot:

```bash
pip install djangorestframework-simplejwt
```

### 2. Configurar o settings.py

Registramos o SimpleJWT como a classe de autenticação padrão da API e definimos os tempos de expiração dos tokens:

```bash
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),   # Sessão ativa por 1 dia
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Renovação automática por até 7 dias
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
}
```


### 3. Proteger Views

Utilizamos a classe IsAuthenticatedOrReadOnly do DRF. Ela blinda as ViewSets de forma que requisições de leitura (GET) permaneçam públicas, enquanto requisições de escrita (POST, PUT, DELETE) passem a exigir o token no cabeçalho:

```bash
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Proteção da rota

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Proteção da rota
```

### 4. Criação dos Endpoints de Autenticação (setup/urls.py)

```bash
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ... rotas anteriores
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

```


