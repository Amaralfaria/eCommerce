document.addEventListener('DOMContentLoaded', function () {
    // Obtém os produtos comprados por meio da API
    function obterProdutosComprados() {
        // Substitua pela lógica de chamada da API para obter produtos comprados
        var token = localStorage.getItem("access_token")
        fetch('http://localhost:8000/cliente/compras',{
            method: 'GET',
            headers: {
                "accept": "application/json",
                'Authorization': `Bearer ${token}`,
            }
        })
            .then(response => response.json())
            .then(compras => {
                // Chama a função para exibir os produtos na lista
                exibirProdutosComprados(compras.Compras);
            })
            .catch(error => {
                console.error('Erro ao obter compras:', error);
            });
    }

    // Exibe os produtos na lista
    function exibirProdutosComprados(compras) {
        var productList = document.getElementById('productList');

        compras.forEach(compra => {
            // Adiciona a data da compra
            // var compraTitle = document.createElement('h2');
            // var conteudo = 
            // compraTitle.textContent = 'Data da Compra: ' + compra.data_compra; // Substitua pelo campo correto
            // productList.appendChild(compraTitle);

            // Para cada produto na compra, obtém detalhes do produto
            compra.produtos.forEach(produtoId => {
                fetch(`http://localhost:8000/produtos/${produtoId}`)
                    .then(response => response.json())
                    .then(produto => {
                        // Chama a função para adicionar o produto à lista
                        adicionarProduto(produto);
                    })
                    .catch(error => {
                        console.error(`Erro ao obter detalhes do produto ${produtoId}:`, error);
                    });
            });
        });
    }

    // Adiciona um produto à lista
    function adicionarProduto(produto) {
        var productList = document.getElementById('productList');

        var listItem = document.createElement('li');
        listItem.classList.add('product');

        var productDetails = document.createElement('div');
        productDetails.classList.add('product-details');

        var productTitle = document.createElement('div');
        productTitle.classList.add('product-title');
        productTitle.textContent = produto.nome; // Substitua pelo campo correto

        var productPrice = document.createElement('div');
        productPrice.classList.add('product-price');
        productPrice.textContent = 'Preço: ' + produto.preco; // Substitua pelo campo correto

        productDetails.appendChild(productTitle);
        productDetails.appendChild(productPrice);

        listItem.appendChild(productDetails);

        // Adicione a imagem do produto, se aplicável
        if (produto.imagem) {
            var productImage = document.createElement('img');
            productImage.src = produto.imagem; // Substitua pelo campo correto
            productImage.alt = produto.nome; // Substitua pelo campo correto
            listItem.insertBefore(productImage, productDetails);
        }

        productList.appendChild(listItem);
    }

    // Chama a função para obter os produtos comprados ao carregar a página
    obterProdutosComprados();
});