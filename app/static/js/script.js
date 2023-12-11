document.addEventListener('DOMContentLoaded', function() {
    fetchProdutos();
});

function cadastrarUsuario(){
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var is_fornecedor = document.getElementById("is_fornecedor").value;
    var telefone = document.getElementById("telefone").value;

    // Monta os dados do novo usuário
    var novoUsuario = {
        "username": username,
        "email": email,
        "password": password,
        "telefone": telefone,
        "is_fornecedor": is_fornecedor,
        "is_cliente": !is_fornecedor
    };


    fetch('http://localhost:8000/usuarios/',{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "accept": "application/json"
        },
        body: JSON.stringify(novoUsuario)
    })
        .then(response => {
            if (response.status === 201) {
                console.log(201)
                window.location.href = 'http://localhost:8000/';
            } else {
                throw new Error('Erro na requisição: ' + response.status);
            }
        })
}

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
