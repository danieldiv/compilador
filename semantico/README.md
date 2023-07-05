# Problema proposto

- Ler um arquivo em linguagem C, realizar análise lexica, sintática e semântica
- Com o código validado, gerar código intermediário
- Após isso, transformar para python

## Léxico

> Consiste em verificar se os caracteres são válidos, como está sendo utilizado `regex`, irá aceitar apenas o que está definido.

### Tipos de caracteres aceitos

- `\w`: letras maiúsculas, minúsculas e números
- `()`: parênteses
- `{}`: chaves
- `//`: comentário
- `;`: para fim de linha
- operadores lógicos
- operadores aritméticos
- operador de atribuição

## Sintático

> Nesta parte é feita a verificação da expressão, por exemplo, a expressão `int x = "teste";` não é valida, mas faz sentido a sua organização, quem irá validar os tipos entre outras coisas é o semântico.

### Funcionamento

- Foi utilizada a linguagem Python para fazer todo o script
- Definição do regex que serão utilizados
- Abrir arquivo para realizar verificação
- Para cada linha testar todos os regex, se algum for válido, então a expressão é válida.

## Semântico

> Necessário para verificar escopo de função, tipos de retornos e declarações.

### Validações

- Escopo de função para declaracao de variáveis
- Escopo de função para declaracao de funções
- Retorno de funções para tipo especifico
- Repetição de variáveis e funções
- Validar tipo de variável declarada

# Funcionamento

> Para melhor organização o código foi separado em modulos, sendo eles:

- static
- sintatic
- main
- semantico
- scope
- parameters


## Arquivo

- Abrir arquivo `códigoX.txt` localizado em `/teste`
- Validar sintaticamente o que já valida lexicamente
- Com a validação, adicionar linha lida em uma lista
- Se a linha não for valida, apresentar mensagem de erro indicando sua localização

## Semântico

- Separar entradas, adicionando uma na lista de includes e outra na lista de funções, cada função possui sua lista de escopo.

## Escopo

> Existem dois tipos de escopo, sendo o primeiro o da função e o segundo o escopo da condicional, que só pode existir dentro do escopo da função.

- O escopo inicia com `{` e finaliza com `}`.

## Parameters

> O escopo da função pode possuir variáveis nos parâmetros, portanto é necessário avaliar a validar antes de entrar no corpo da função.

## Body (corpo)

> Todo o corpo da função é uma lista com informação sobre a linha e conteúdo. Estruturas condicionais também ficam na lista do corpo, porém de maneira diferente.

## Return

> Realiza a verificação da validade do retorno

## Dificuldades e  Observações

> O arquivo `static.py` contem funções e variáveis fixas para serem utilizadas em todo o código.

- Criação dos `regexs`
- Revalidação dos `regexs` para atender o código fornecido pelo professor
- Complexidade de validações, sendo necessário criar vários módulos
- Como a estrutura condicional é diferente de um escopo comum, ela não é tratada `semanticamente`.
- Múltiplas operações não são tratadas.

## Transpilar de C para Python

> Se houver tempo hábil, faremos. 