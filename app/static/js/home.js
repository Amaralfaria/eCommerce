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
    // latitude = localStorage.getItem()
    // // Substitua pela lógica de chamada da API para obter produtos

    // url = 'http://localhost:8000/produtos/?'

    // url += localStorage.getItem("latitude");
    // url += '&'
    // url +=

    

    fetch('http://localhost:8000/produtos/?latitudeCliente=50.1&longitudeCliente=50.1')
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

    produtos.forEach(produto => {
        var productCard = document.createElement('a'); // Transforma o card em um link
        productCard.href = `http://localhost:8000/visualizar_produto/${produto.id}`; // Substitua pela URL correta
        productCard.classList.add('product-card');

        var productName = document.createElement('h2');
        var distanciaProduto = document.createElement('p')
        productName.textContent = produto.nome; // Substitua pelo campo correto
        distanciaProduto.textContent = produto.distancia



        // Adicione a imagem do produto, se aplicável
        if (produto.imagem) {
            var productImage = document.createElement('img');
            productImage.src = produto.imagem; // Substitua pelo campo correto
            productImage.alt = produto.nome; // Substitua pelo campo correto
            productCard.appendChild(productImage);
        }

        productCard.appendChild(productName);
        productCard.appendChild(distanciaProduto);
        productContainer.appendChild(productCard);
    });
}