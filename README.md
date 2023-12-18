# MP-Backend

## Executando o projeto

1 - Primeiro instale as dependencias, para isso execute o comando abaixo:

```sh
    pip install -r requirements.txt
```

2 - Execute o servidor. Para isso execute o comando abaixo no diretorio src:
```sh
    make start
```
3 - Com o servidor executando va para o endpoint:
```sh
    home/
```
Caso não tenha o make instalado, basta executar o comando:
```sh
    python3 manage.py runserver
```

## Executando os testes

1 - Descomentar de trabalho_mp/settings.py por questões de autenticação a linha:
```sh
    158: "rest_framework.authentication.SessionAuthentication",
```

2 - Execute o comando abaixo no diretorio src:
```sh
    make test
```


## Documentação das APIs

Para acessar a documentação utilizar o endpoint:
```sh
    schema/docs/
```

## Relatorio de testes
O relatório está em:
```sh
    src/htmlcov/index.html
```



