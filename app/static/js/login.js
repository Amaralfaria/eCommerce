function login() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    const homeUrl = '/'; // URL da página inicial


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
        if (response.status === 200) {
            return response.json();
        } else {
            response.json().then(data => {
                alert(data.detail || 'Erro ao fazer login. Verifique suas credenciais.');
            });
            throw new Error('Erro na autenticação: ' + response.status);
        }
    })
    .then(data => {
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        alert('Login bem-sucedido!');
        window.location.href = 'http://localhost:8000/home/'; // Redirecionamento para a página inicial
    })
    .catch(error => {
        console.error('Erro na autenticação:', error);
    });
}