document.addEventListener('DOMContentLoaded', function (){
    preencherFeiras();
})

function criarFornecedor() {
    var nomeNegocio = document.getElementById('nome_negocio').value;
    var endereco = document.getElementById('endereco').value;
    var latitude = document.getElementById('latitude').value;
    var longitude = document.getElementById('longitude').value;
    var feira = document.getElementById('feira').value;
    var token = localStorage.getItem("access_token");

    var dadosFornecedor = {
        "nome_do_negocio": nomeNegocio,
        "endereco": endereco,
        "latitude": latitude,
        "longitude": longitude,
        "feira": feira
    };

    // Fazer a solicitação POST usando Fetch API
    fetch('http://localhost:8000/fornecedores/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "accept": "application/json",
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(dadosFornecedor),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro na requisição: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log('Resposta da API:', data);
        alert('Fornecedor criado com sucesso!');
    })
    .catch(error => {
        console.error('Erro na criação do fornecedor:', error);
        alert('Erro ao criar o fornecedor. Verifique os dados e tente novamente.');
    });
}

function preencherFeiras() {
    var feiraSelect = document.getElementById('feira');

    // Fazer solicitação para a API que retorna a lista de feiras
    fetch('http://localhost:8000/feira/')
        .then(response => response.json())
        .then(feiras => {
            // Preencher o campo de seleção com as feiras disponíveis
            feirajson = feiras.feiras
            feirajson.forEach(feira => {
                var option = document.createElement('option');
                option.value = feira.id; // Suponha que cada feira tenha um ID
                option.text = feira.nome; // Suponha que cada feira tenha um campo "nome"
                feiraSelect.add(option);
                console.log(option)
            });
        })
        .catch(error => {
            console.error('Erro ao obter a lista de feiras:', error);
        });
}

