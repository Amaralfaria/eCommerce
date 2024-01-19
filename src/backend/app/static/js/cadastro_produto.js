document.addEventListener('DOMContentLoaded', function () {
    // Preenche o select de categorias dinamicamente

    // Chama a função para preencher as categorias ao carregar a página
    preencherCategorias();
});

function preencherCategorias() {
    var categoriaSelect = document.getElementById('categoria');

    // Fazer solicitação para a API que retorna a lista de categorias
    fetch('http://localhost:8000/categorias/')
        .then(response => response.json())
        .then(categorias => {
            // Preencher o campo de seleção com as categorias disponíveis
            categoriasjson = categorias.categorias
            console.log(categoriasjson)
            categoriasjson.forEach(categoria => {
                var option = document.createElement('option');
                option.value = categoria.id; // Suponha que cada categoria tenha um ID
                option.text = categoria.nome; // Suponha que cada categoria tenha um campo "nome"
                categoriaSelect.add(option);
            });
        })
        .catch(error => {
            console.error('Erro ao obter a lista de categorias:', error);
        });
}

function cadastrarProduto() {
    // Coleta os dados do formulário
    var nome = document.getElementById('nome').value;
    var descricao = document.getElementById('descricao').value;
    var preco = document.getElementById('preco').value;
    var categoria = document.getElementById('categoria').value;
    var imagem = document.getElementById('imagem_produto').files[0]
    var token = localStorage.getItem("access_token")
    var formData = new FormData();
    formData.append('nome',nome)
    formData.append('descricao',descricao)
    formData.append('preco',preco)
    formData.append('categoria',categoria)
    formData.append('imagem',imagem)

    // Monta os dados do novo produto
    // var novoProduto = {
    //     "nome": nome,
    //     "descricao": descricao,
    //     "preco": preco,
    //     "categoria": categoria,
    //     "imagem": imagem,
    // };

    // Fazer a solicitação POST usando Fetch API
    fetch('http://localhost:8000/produtos/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
        body: formData
        // body: JSON.stringify(novoProduto),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro na requisição: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log('Resposta da API:', data);
        alert('Produto cadastrado com sucesso!');
        window.location.href = 'http://localhost:8000/home/'
    })
    .catch(error => {
        console.error('Erro no cadastro do produto:', error);
        alert('Erro ao cadastrar o produto. Verifique os dados e tente novamente.');
    });
}