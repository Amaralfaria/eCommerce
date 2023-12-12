function cadastrarUsuario(){
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var is_fornecedor = document.getElementById("is_fornecedor").checked;
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
                const urlToken = 'http://localhost:8000/token/'

                var credencials = {
                    "username": username,
                    "password": password,
                }

                return fetch(urlToken,{
                    method: "POST",
                    headers:{
                        "Content-Type": "application/json",
                        "accept": "application/json"
                    },
                    body: JSON.stringify(credencials)
                })
            } else {
                throw new Error('Erro na requisição: ' + response.status);
            }
        })
        .then(response => response.json())
        .then(token => {
            localStorage.setItem("access_token",token.access);
            localStorage.setItem("refresh_token",token.refresh);

            if(!is_fornecedor){
                const urlClient = 'http://localhost:8000/cliente/'
                
                novo_cliente = {
                    "preferencias_de_busca": null
                }
    
                return fetch(urlClient,{
                    method: "POST",
                    headers:{
                        "Content-Type": "application/json",
                        "accept": "application/json",
                        'Authorization': `Bearer ${token.access}`,
                    },
                    body : JSON.stringify(novo_cliente)
                })
            }else{
                window.location.href = 'http://localhost:8000/criar_fornecedor/'
            }


        })
        .then(response => {
            if(response.status == 201){
                window.location.href = 'http://localhost:8000/home/';
            }else{
                console.log('Erro ao criar cliente')
            }
        })
}

// 