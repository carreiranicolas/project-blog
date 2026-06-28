import { useState, useEffect } from 'react';
import api from './services/api'; // Importamos a nossa configuração do Axios

function App() {
  // Criamos o estado 'posts' iniciando como uma lista vazia []
  // 'setPosts' é a função que usaremos para atualizar essa lista depois
  const [posts, setPosts] = useState([]);

  // O useEffect vai rodar assim que a página carregar
  useEffect(() => {
    // Criamos uma função assíncrona para buscar os posts
    const buscarPosts = async () => {
      try {
        // O Axios junta o '/' com a baseURL, virando 'http://localhost:8000/posts/'
        const resposta = await api.get('/posts/');
        
        // No Axios, os dados que o servidor enviou ficam sempre dentro de .data
        console.log("Dados que vieram do Django:", resposta.data);
        
        // Salvamos os posts no nosso estado para o React tomar conhecimento
        setPosts(resposta.data);
      } catch (error) {
        console.error("Erro ao buscar posts do backend:", error);
      }
    };

    buscarPosts();
  }, []); // Essa lista vazia [] no final garante que o useEffect só rode UMA vez no carregamento

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Blog do Nicolas 🚀</h1>
      <h2>Testando Conexão com o Backend</h2>
      
      {/* Se a lista estiver vazia, mostra um aviso */}
      {posts.length === 0 ? (
        <p>Nenhum post encontrado ou backend desligado...</p>
      ) : (
        /* Se tiver posts, fazemos um mapa (loop) para renderizar cada um na tela */
        posts.map((post) => (
          <div key={post.id} style={{ border: '1px solid #ccc', padding: '15px', marginBottom: '10px', borderRadius: '5px' }}>
            <h3>{post.titulo}</h3>
            <p>{post.descricao}</p>
            <small>Por: <strong>{post.autor_nome}</strong></small>
          </div>
        ))
      )}
    </div>
  );
}

export default App;