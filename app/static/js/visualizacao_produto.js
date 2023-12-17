document.addEventListener('DOMContentLoaded', function () {
    // URL da primeira API (substitua pela sua URL real)
    displayFormAvaliacao();
    id = document.getElementById('id_produto').textContent
    const firstApiUrl = `http://localhost:8000/produtos/${id}`;

    // Elemento onde as informações do produto serão exibidas
    const productContainer = document.getElementById('productContainer');

    // Variável para armazenar as informações do produto
    let productInfo;

    // Função para buscar dados da primeira API
    fetch(firstApiUrl)
        .then(response => response.json())
        .then(product => {
            // Armazenar as informações do produto
            productInfo = product;

            // Obter o ID do fornecedor do primeiro API
            const fornecedorId = product.fornecedor;

            // URL da segunda API para obter o nome do fornecedor (substitua pela sua URL real)
            const secondApiUrl = `http://localhost:8000/fornecedores/${fornecedorId}`;
            
            // Fazer solicitação para a segunda API
            return fetch(secondApiUrl);
        })
        .then(response => response.json())
        .then(fornecedor => {
            fornecedorInfo = fornecedor
            const thirdApiUrl = `http://localhost:8000/categorias/${productInfo.categoria}`;
            
            return fetch(thirdApiUrl)
        })
        .then(response => response.json())
        .then(categoria =>{
            // Atualizar o conteúdo do contêiner com as informações do produto e do fornecedor
            productContainer.innerHTML = `
                <h1>${productInfo.nome}</h1>
                <p class="description">Descrição: ${productInfo.descricao}</p>
                <p class="category">Categoria: ${categoria.nome}</p>
                <p class="supplier">Fornecedor: ${fornecedorInfo.nome_do_negocio}</p>
                <p class="price">Preço: R$ ${productInfo.preco}</p>
            `;
            
            if(localStorage.getItem("tipo_usuario") === "cliente"){
                productContainer.innerHTML += `<a href="#" class="buy-button" onclick="comprarProduto()">Comprar</a>
                <a href="#" class="buy-button" onclick="irParaChat(${fornecedorInfo.fornecedor_user})">Conversar com vendedor</a>`;
            }
        })
        .catch(error => console.error('Erro ao obter dados da API:', error));

        carregarAvaliacoesDaAPI()
});

function irParaChat(idFornecedor){
    window.location.href = `http://localhost:8000/chat/${idFornecedor}`;
}

function exibirAvaliacoes(avaliacoes) {
    const reviewsList = document.getElementById('reviewsList');
    reviewsList.innerHTML = ''; // Limpar a lista antes de adicionar novas avaliações

    avaliacoes.forEach(avaliacao => {
        const reviewDiv = document.createElement('div');
        reviewDiv.classList.add('review');


        const reviewTitle = document.createElement('h3');

        carregaClienteAvaliacao(avaliacao.cliente)
            .then(username => {
                reviewTitle.textContent = username;
            })


        const reviewComment = document.createElement('p');
        reviewComment.textContent = avaliacao.comentario;

        const reviewRating = document.createElement('p');
        reviewRating.textContent = `Nota: ${avaliacao.nota}`;

        reviewDiv.appendChild(reviewTitle);
        reviewDiv.appendChild(reviewComment);
        reviewDiv.appendChild(reviewRating);

        reviewsList.appendChild(reviewDiv);
    });
}

function carregaClienteAvaliacao(idCliente){
    const urlAPI = `http://localhost:8000/cliente/${idCliente}`;

    return fetch(urlAPI)
        .then(response => response.json())
        .then(cliente => {
            const idUsuario = cliente.cliente_user;
            const urlUsuario = `http://localhost:8000/usuarios/${idUsuario}`;

            return fetch(urlUsuario)
        })
        .then(response => response.json())
        .then(usuario => {
            return usuario.username
        })
}

function carregarAvaliacoesDaAPI() {
    const idProduto = document.getElementById('id_produto').textContent;

    // Substitua a URL abaixo pela sua URL de API real
    const urlAPI = `http://localhost:8000/avaliacoes_produto/${idProduto}`;

    fetch(urlAPI)
        .then(response => response.json())
        .then(data => {
            // console.log(data.avaliacoes)
            exibirAvaliacoes(data.avaliacoes);
        })
        .catch(error => console.error('Erro ao carregar avaliações da API:', error));
}

// Carregar avaliações ao carregar a página
document.addEventListener('DOMContentLoaded', function () {
    carregarAvaliacoesDaAPI();
});

function criarAvaliacao(){
    var comentario = document.getElementById("reviewComment").value;
    var nota = document.getElementById("reviewRating").value;
    var token = localStorage.getItem("access_token")
    var id_produto = document.getElementById("id_produto").textContent

    // Monta os dados do novo usuário
    var nova_avaliacao = {
        "comentario": comentario,
        "nota": parseInt(nota),
        "produto": parseInt(id_produto)
    }

    // console.log(nova_avaliacao)


    fetch(`http://localhost:8000/avaliacoes/`,{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "accept": "application/json",
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(nova_avaliacao)
    })
        .then(response => {
            if (response.status === 201) {
                // console.log(response)
                window.location.reload()
            } else {
                throw new Error('Erro na requisição: ' + response.status);
            }
        })
}

function comprarProduto(){
    var dataAtual = new Date();

    // Use a função toISOString para obter a data formatada como "YYYY-MM-DD"
    var dataFormatada = dataAtual.toISOString().split('T')[0];

    var nova_compra = {
        "data_compra": dataFormatada,
        "produtos": [
            parseInt(document.getElementById("id_produto").textContent)
        ]
    }

    var token = localStorage.getItem("access_token")

    fetch(`http://localhost:8000/cliente/compras/`,{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "accept": "application/json",
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(nova_compra)
    })
        .then(response => {
            if (response.status === 201) {
                window.location.href = 'http://localhost:8000/produtos_comprados/'
            } else {
                throw new Error('Erro na requisição: ' + response.status);
            }
        })
}

function displayFormAvaliacao(){
    if(localStorage.getItem("tipo_usuario") !== "cliente"){
        document.getElementById("createReviewForm").style.display = 'none';
    }
}