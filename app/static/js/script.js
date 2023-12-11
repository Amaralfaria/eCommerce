document.addEventListener('DOMContentLoaded', function() {
    fetchProdutos();
});

function fetchProdutos() {
    fetch('http://localhost:8000/produtos/')
        .then(response => response.json())
        .then(data => displayProdutos(data.produtos))
        .catch(error => console.error('Erro ao buscar produtos:', error));
}

function displayProdutos(produtos) {
    const container = document.getElementById('lista-produtos');
    container.innerHTML = ''; // Limpa a lista atual
    produtos.forEach(produto => {
        const div = document.createElement('div');
        div.innerHTML = `<h3>${produto.nome}</h3><p>R$ ${produto.preco}</p>`;
        container.appendChild(div);
    });
}

function pesquisarProdutos() {
    let termo = document.getElementById('barra-pesquisa').value;
    fetch(`http://localhost:8000/produtos/?nomeProduto=${termo}`) // Adapte para a sua URL de pesquisa
        .then(response => response.json())
        .then(data => displayProdutos(data.produtos))
        .catch(error => console.error('Erro ao pesquisar produtos:', error));
}
