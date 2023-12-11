function login() {
    // Obtenha os valores do usuário e senha
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    console.log(username)
    console.log(password)

    // Dados a serem enviados no corpo da solicitação
    var dados = {
        "username": username,
        "password": password
    };

    fetch('http://localhost:8000/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "accept": "application/json",
        },
        body: JSON.stringify(dados)
    })
    .then(response => {
        if (response.status != 200) {
            alert('Usuario não encontrado!');
            throw new Error('Erro na login: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        // Lógica de sucesso - manipule a resposta da API conforme necessário
        localStorage.setItem("access_token",data.access)
        localStorage.setItem("refresh_token",data.refresh)
        alert('Login bem-sucedido!'); // Adapte conforme necessário
    })
    .catch(error => {
        // Lógica de erro - manipule os erros da API
        console.error('Erro na autenticação:', error);
        alert('Erro ao fazer login. Verifique suas credenciais.');
    });
}