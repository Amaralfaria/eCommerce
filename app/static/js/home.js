document.addEventListener('DOMContentLoaded', function() {
    obterProdutos()
});

// function fetchProdutos() {
//     fetch('http://localhost:8000/produtos/')
//         .then(response => response.json())
//         .then(data => displayProdutos(data.produtos))
//         .catch(error => console.error('Erro ao buscar produtos:', error));
// }

// function displayProdutos(produtos) {
//     const container = document.getElementById('lista-produtos');
//     container.innerHTML = ''; // Limpa a lista atual
//     produtos.forEach(produto => {
//         const div = document.createElement('div');
//         div.innerHTML = `<h3>${produto.nome}</h3><p>R$ ${produto.preco}</p>`;
//         container.appendChild(div);
//     });
// }

// function pesquisarProdutos() {
//     let termo = document.getElementById('barra-pesquisa').value;
//     fetch(`http://localhost:8000/produtos/?nomeProduto=${termo}`) // Adapte para a sua URL de pesquisa
//         .then(response => response.json())
//         .then(data => displayProdutos(data.produtos))
//         .catch(error => console.error('Erro ao pesquisar produtos:', error));
// }


function obterProdutos() {

    url = 'http://localhost:8000/produtos/'

    url += `?latitudeCliente=${localStorage.getItem("latitude")}&longitudeCliente=${localStorage.getItem("longitude")}`;

    raio = document.getElementById('raio').value
    fornecedor = document.getElementById('nome_fornecedor').value
    produto = document.getElementById('barra-pesquisa').value
    precoMaximo = document.getElementById('precoMaximo').value
    precoMinimo = document.getElementById('precoMinimo').value


    
    if(raio){
        url += `&raio=${raio}`;
    }

    if(produto){
        url += `&nomeProduto=${produto}`;
    }

    if(fornecedor){
        url += `&banca=${fornecedor}`;
    }

    if(precoMaximo){
        url += `&precoMaximo=${precoMaximo}`;
    }

    if(precoMinimo){
        url += `&precoMinimo=${precoMinimo}`;
    }
    
    

    fetch(url)
        .then(response => response.json())
        .then(produtos => {
            // Chama a função para exibir os produtos
            exibirProdutos(produtos.produtos);
        })
        .catch(error => {
            console.error('Erro ao obter produtos:', error);
        });
}

// Exibe os produtos na lista
function exibirProdutos(produtos) {
    var productContainer = document.getElementById('productContainer');
    productContainer.innerHTML = '';

    produtos.forEach(produto => {
        var productCard = document.createElement('a'); // Transforma o card em um link
        productCard.href = `http://localhost:8000/visualizar_produto/${produto.id}`; // Substitua pela URL correta
        productCard.classList.add('product-card');

        var productName = document.createElement('h2');
        var distanciaProduto = document.createElement('p')
        var preco = document.createElement('p')
        productName.textContent = produto.nome; // Substitua pelo campo correto
        distanciaProduto.textContent = produto.distancia
        preco.textContent = produto.preco



        // Adicione a imagem do produto, se aplicável
        if (produto.imagem) {
            var productImage = document.createElement('img');
            productImage.src = produto.imagem; // Substitua pelo campo correto
            productImage.alt = produto.nome; // Substitua pelo campo correto
            productCard.appendChild(productImage);
        }

        productCard.appendChild(productName);
        productCard.appendChild(distanciaProduto);
        productCard.appendChild(preco);
        productContainer.appendChild(productCard);
    });
}