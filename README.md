# Motinha VRUUMM - Marketplace de Peças de Moto

Este projeto é uma aplicação web desenvolvida como parte da disciplina de Estrutura de Dados e Análise de Algoritmos (EDA). "Motinha VRUUMM" é um marketplace fictício que permite a busca e venda de peças de motocicleta, implementando diferentes algoritmos de busca para otimizar a performance da aplicação.

## Alunos

- **Caio Mesquita** - Matrícula: 222024283
- **Manoel Teixeira** - Matrícula: 211041240

## Vídeo da Apresentação

[Clique Aqui](https://youtu.be/ecDIGzC7I8o) para assistir o vídeo

## Sobre o Projeto

O "Motinha VRUUMM" é uma plataforma robusta que simula um e-commerce de peças para motocicletas. A aplicação foi construída utilizando Flask, um micro-framework em Python, e emprega a biblioteca Pandas para manipulação de dados. O objetivo principal do projeto é demonstrar a aplicação prática de diferentes algoritmos de busca em um cenário real, visando a eficiência e a rapidez na recuperação de informações de um grande catálogo de produtos.

### Funcionalidades

O marketplace oferece as seguintes funcionalidades de busca:

* **Busca por ID (SKU):** Encontra peças rapidamente a partir de um prefixo de SKU.
* **Filtragem por Atributos:** Permite que os usuários filtrem peças por marca, modelo, categoria e ano.
* **Busca por Faixa de Preço:** Pesquisa por peças dentro de um intervalo de preço específico, podendo ser combinada com outros filtros.

## Algoritmos de Busca Utilizados

A eficiência da plataforma é garantida pela escolha estratégica de algoritmos de busca para cada tipo de consulta, conforme detalhado abaixo:

### 1. Busca por ID (SKU) - Busca Binária

-   **Arquivo:** `algoritmos/busca_binaria.py`
-   **Descrição:** Para a busca por prefixo de SKU (ID do produto), foi implementada a **Busca Binária**. Antes da aplicação iniciar, o DataFrame de peças é ordenado pelo SKU. Isso permite que, ao buscar por um prefixo, o algoritmo localize rapidamente o ponto de partida para os SKUs correspondentes usando `bisect_left`. A partir desse ponto, ele percorre a lista sequencialmente apenas enquanto os SKUs corresponderem ao prefixo.
-   **Justificativa:** A busca binária tem uma complexidade de tempo de **O(log n)** para encontrar o ponto inicial, o que é extremamente eficiente para grandes conjuntos de dados ordenados, superando com folga a busca linear que teria complexidade O(n).

### 2. Filtragem por Atributos - Hashing

-   **Arquivo:** `algoritmos/busca_hash.py`
-   **Descrição:** A filtragem por múltiplos critérios (Marca, Modelo, Ano, Categoria) utiliza o conceito de **hashing**. Na inicialização, são criados índices (dicionários Python) para cada um desses atributos. Cada chave do dicionário corresponde a um valor de filtro (ex: "Honda") e armazena uma lista de índices do DataFrame original onde esse valor ocorre. Ao aplicar múltiplos filtros, a busca é feita pegando os índices do primeiro filtro e realizando operações de **interseção** com os conjuntos de índices dos filtros subsequentes.
-   **Justificativa:** A busca em uma tabela de hash tem complexidade de tempo média de **O(1)**. A operação de interseção de conjuntos também é altamente otimizada. Isso torna a filtragem combinada quase instantânea, mesmo com um grande volume de dados.

### 3. Busca por Faixa de Preço - Busca Linear com Filtragem

-   **Arquivo:** `algoritmos/busca_preco.py`
-   **Descrição:** A busca por preço é realizada através de uma **filtragem linear** no DataFrame do Pandas. O algoritmo seleciona todas as peças que atendem aos critérios de preço mínimo e/ou máximo fornecidos pelo usuário. Esta função também foi aprimorada para incorporar os filtros de atributos (marca, modelo, etc.), aplicando-os antes da filtragem por preço para reduzir o conjunto de dados a ser percorrido.
-   **Justificativa:** Como os preços não são o principal critério de ordenação e a busca é por uma faixa, uma busca linear sobre o conjunto de dados (potencialmente pré-filtrado) é uma abordagem direta e eficaz. A integração com os filtros de hash otimiza o processo, diminuindo o número de comparações necessárias.

## Como Rodar o Projeto

Para executar o projeto em sua máquina local, siga os passos abaixo.

### Pré-requisitos

-   Python 3.x
-   `pip` (gerenciador de pacotes do Python)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Instale as dependências:**
    O projeto utiliza as bibliotecas listadas no arquivo `requirements.txt`. Para instalá-las, execute o comando:
    ```bash
    pip install -r requirements.txt
    ```

### Execução

1.  **Verifique os arquivos:**
    Certifique-se de que o arquivo `motoparts.csv` está na raiz do projeto, no mesmo diretório que o `app.py`.

2.  **Inicie a aplicação Flask:**
    Com as dependências instaladas, execute o seguinte comando no terminal:
    ```bash
    flask run
    ```
    Ou, alternativamente:
    ```bash
    python app.py
    ```

3.  **Acesse a aplicação:**
    Abra o seu navegador e acesse o endereço fornecido no terminal, que geralmente é:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

A aplicação estará rodando e pronta para uso.
