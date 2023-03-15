# Commission Calc
    O `commission Calc` é uma aplicação criada com o intuito de realizar o cálculos de comissões dentro de vendas encontradas no programa `ContaAzul`.

## Pré-requisitos
    O `Commission Calc` pode ser inicializado de duas maneiras:
    * ``Python``: > 3.10
    Ou
    * ``Docker``: > 20.10.21

## Setup do projeto
    Para utilizar o projeto, é necessário baixar uma das versões com TAG.
    Com a versão deseja baixada, use os comandos abaixos listados para cada caso de inicialização:
    * Python:
    ```python
        # ./app
        # Linux:
        python3 -u src/main.py

        # Windows:
        python -u src/main.py
    ```
    
    * Docker:
    ```
        # Caso docker-compose esteja instalado:
        docker-compose up --build

        # Caso contrário:
        docker build -t commission-calc .
        docker run -p 3000:3000 --name commission-calc commission-calc 
    ```

## Configurações
    O arquivo `app.env` possui as variáveis necessárias para que o projeto funcione.
    Nele, há 2 comentários: "Public" e "Devs".
    O "Public" possuirá todas as variáveis que comumente são alteradas a cada vez que o programa é inicializado.
    Enquanto o "Devs" possui variáveis que o código irá utilizar dentro de sua lógica. Apenas altere-os caso saiba o que esteja fazendo!

## Uso
    Com o projeto ligado, será necessário acessar o `localhost:3000`.
    Ele irá te redirecionar para a autenticação do ContaAzul, questionando sobre as permissões do aplicativo dentro de suas contas.
    Com a permissão garantida, o servidor irá pegar todas as vendas realizadas dentro do período fornecido no `app.env`.
    O resultado é retornado no formato de download, com o arquivo `result.xlsx`.