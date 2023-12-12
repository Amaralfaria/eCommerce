document.addEventListener('DOMContentLoaded', function () {
    const conversationsContainer = document.getElementById('conversationsContainer');

    // Função para obter as conversas da API
    function obterConversas() {
        var token = localStorage.getItem("access_token");
        // Substitua pela lógica de chamada da API para obter conversas
        fetch('http://localhost:8000/mensagens_fornecedor/',{
            method: "GET",
            headers:{
                "accept": "application/json",
                'Authorization': `Bearer ${token}`,
            }
        })
            .then(response => response.json())
            .then(conversas => {
                // Chama a função para exibir as conversas
                exibirConversas(conversas.usuarios);
            })
            .catch(error => {
                console.error('Erro ao obter conversas:', error);
            });
    }

    // Função para exibir as conversas na tela
    function exibirConversas(conversas) {
        conversationsContainer.innerHTML = ''; // Limpa as conversas anteriores

        conversas.forEach(conversa => {
            const userCard = document.createElement('a'); // Transforma o card em um link
            userCard.href = `http://localhost:8000/chat/${conversa.remetente_id}`; // Substitua pela URL correta
            userCard.classList.add('user-card');

            const userAvatar = document.createElement('div');
            userAvatar.classList.add('user-avatar');
            // Adicione a lógica para carregar a imagem do avatar, se aplicável
            userCard.appendChild(userAvatar);

            const userInfo = document.createElement('div');
            userInfo.classList.add('user-info');

            const userName = document.createElement('h3');
            userName.textContent = conversa.remetente__username; // Substitua pelo campo correto

            const lastMessage = document.createElement('p');
            lastMessage.textContent = conversa.conteudo; // Substitua pelo campo correto

            userInfo.appendChild(userName);
            userInfo.appendChild(lastMessage);
            userCard.appendChild(userInfo);

            conversationsContainer.appendChild(userCard);
        });
    }

    // Chama a função para obter as conversas ao carregar a página
    obterConversas();
});