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