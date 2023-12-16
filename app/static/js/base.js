document.addEventListener('DOMContentLoaded', function () {
    obterEArmazenarLocalizacao();
    // Elemento HTML onde o menu será inserido

    var token = localStorage.getItem("access_token")

    var menuContainer = document.getElementById('menu');

    var tipoMenu = {
        "cliente": [
            {"label": "Home", "url": "http://localhost:8000/home"},
            {"label": "Minhas compras", "url": "http://localhost:8000/produtos_comprados/"},
            {"label": "Minhas conversas", "url": "http://localhost:8000/conversas/"},
            {"label": "Login", "url": "http://localhost:8000/login/"},
        ],
        "fornecedor": [
            {"label": "Home", "url": "http://localhost:8000/home"},
            {"label": "Cadastrar produto", "url": "http://localhost:8000/criar_produto/"},
            {"label": "Minhas conversas", "url": "http://localhost:8000/conversas/"},
            {"label": "Login", "url": "http://localhost:8000/login/"},
        ],
        "anonimo": [
            {"label": "Home", "url": "http://localhost:8000/home"},
            {"label": "Login", "url": "http://localhost:8000/login/"},
        ],
    };

    // URL da API que fornece os itens do menu
    var apiUrl = 'http://localhost:8000/usuario/tipo/';

    if(token === null || token === 'undefined'){
        menuItems = tipoMenu["anonimo"]
        var menuList = document.createElement('ul');
        menuItems.forEach(function (menuItem) {
            var listItem = document.createElement('li');
            var link = document.createElement('a');
            link.href = menuItem.url;
            link.textContent = menuItem.label;
            listItem.appendChild(link);
            menuList.appendChild(listItem);
        });

        // Adiciona a lista de menu ao contêiner
        menuContainer.appendChild(menuList);
    }else{
    

        // Realiza a requisição à API
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "accept": "application/json",
                'Authorization': `Bearer ${token}`,
            },
        })
            .then(response => response.json())
            .then(data => {
                menuItems = tipoMenu[data.tipo]
                console.log(menuItems)
                // Manipula os dados recebidos da API
                if (data) {
                    // Cria elementos de lista para cada item do menu
                    var menuList = document.createElement('ul');
                    menuItems.forEach(function (menuItem) {
                        var listItem = document.createElement('li');
                        var link = document.createElement('a');
                        link.href = menuItem.url;
                        link.textContent = menuItem.label;
                        listItem.appendChild(link);
                        menuList.appendChild(listItem);
                    });

                    // Adiciona a lista de menu ao contêiner
                    menuContainer.appendChild(menuList);
                } else {
                    console.error('Formato de dados da API inválido.');
                }
            })
            .catch(error => {
                console.error('Erro ao obter dados da API:', error);
            });
    }
});

function obterEArmazenarLocalizacao() {
    // Verifica se o navegador suporta a API de Geolocalização
    if ("geolocation" in navigator) {
        // Obtém e armazena a localização do usuário
        navigator.geolocation.getCurrentPosition(
            function (position) {
                // A posição está disponível
                const localizacao = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };

                // Armazena a localização no localStorage
                localStorage.setItem('latitude', localizacao.latitude);
                localStorage.setItem('longitude', localizacao.longitude);

                console.log('Localização atualizada:', localizacao);
            },
            function (error) {
                // Ocorreu um erro ao obter a posição
                console.error("Erro ao obter a localização:", error.message);
            }
        );
    } else {
        // O navegador não suporta a API de Geolocalização
        console.error("Geolocalização não suportada pelo navegador.");
    }
}

// Chama a função a cada 10 segundos
setInterval(obterEArmazenarLocalizacao, 10000);
