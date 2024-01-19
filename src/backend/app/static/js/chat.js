document.addEventListener('DOMContentLoaded', function () {
    const messagesContainer = document.getElementById('messages-container');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    // Função para buscar mensagens da API
    function obterMensagens() {
        // Substitua pela lógica de chamada da API para obter mensagens
        var token = localStorage.getItem("access_token")
        var idFornecedor = document.getElementById('id_fornecedor').textContent
        fetch(`http://localhost:8000/mensagens/${idFornecedor}`,{
            method: 'GET',
                headers: {
                    "accept": "application/json",
                    'Authorization': `Bearer ${token}`,
                }
        })
            .then(response => response.json())
            .then(mensagens => {
                // Chama a função para exibir as mensagens
                exibirMensagens(mensagens.mensagens);
            })
            .catch(error => {
                console.error('Erro ao obter mensagens:', error);
            });
    }

    // Função para exibir mensagens na tela
    function exibirMensagens(mensagens) {
        messagesContainer.innerHTML = ''; // Limpa as mensagens anteriores

        mensagens.forEach(mensagem => {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message');
            messageElement.textContent = mensagem.conteudo;
            messageElement.classList.add('incoming');
            // if (mensagem.origem === 'incoming') {
            //     messageElement.classList.add('incoming');
            // } else {
            //     messageElement.classList.add('outgoing');
            // }

            messagesContainer.appendChild(messageElement);
        });

        // Rola para baixo para mostrar as mensagens mais recentes
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Função para enviar mensagem para a API
    function enviarMensagem() {

        var mensagem = {
            "destinatario_id": document.getElementById('id_fornecedor').textContent,
            "conteudo": messageInput.value
        }

        var token = localStorage.getItem("access_token")

        if (mensagem.conteudo.trim() !== '') {
            // Substitua pela lógica de chamada da API para enviar mensagem
            fetch('http://localhost:8000/mensagens/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "accept": "application/json",
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(mensagem),
            })
            .then(response => response.json())
            .then(() => {
                // Limpa o campo de entrada após o envio
                messageInput.value = '';
                // Atualiza as mensagens para exibir a mensagem enviada
                obterMensagens();
            })
            .catch(error => {
                console.error('Erro ao enviar mensagem:', error);
            });
        }
    }

    // Chama a função para obter as mensagens ao carregar a página
    obterMensagens();

    // Configura um ouvinte de evento para o botão de envio
    sendButton.addEventListener('click', enviarMensagem);
});