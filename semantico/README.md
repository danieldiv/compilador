# Problema proposto

- Ler um arquivo em linguagem C, realizar analise lexica, sintatica e semantica
- Com o codigo validado, gerar codigo intermediario
- Apos isso, transformar para python

## Lexico

> Consiste em verificar se os caracteres sao validos, como esta sendo utilizado `regex`, irá aceitar apenas o que esta definido.

### Tipos de caracteres aceitos

- `\w`: letras maiusculas e minusculas e numeros
- `()`: parenteses
- `{}`: chaves
- `//`: comentario
- `;`: para fim de linha
- operadores logicos
- operadores aritimeticos
- operador de atribuição

## Sintatico

> Nesta parte é feita a verifição da expressao, por exemplo, a expressao `int x = "teste";` não é valida, mas faz sentido a sua organização, quem irá validar os tipos entre outras coisas é o semantico.

### Funcionamento

- Definição do regex que serão utilizados
- Abrir arquivo para realizar verificação
- Para cada linha testar todos os regex, se algum for valido, entao a expressao é valida.

## Semantico

> Necessario para verificar escopo de funcao, tipos de retornos e declarações.a

### Validacoes

- Escopo de funcao para declaracao de variaveis
- Escopo de funcao para declaracao de funcoes
- Retorno de funcoes para tipo especifico
- Repetição de variaveis e funcoes
- Validar tipo de variavel declarada

# Funcionamento

> Para melhor organização o codigo foi separado em modulos, sendo eles:

- static
- sintatic
- main
- semantico
- scope
- parameters


## Arquivo

- Abrir arquivo `códigoX.txt` localizado em `/teste`
- Validar sintaticamente o que tambem ja valida lexicamente
- Com a validação, adicionar linha lida em uma lista
- Se linha não for valida, apresentar mensagem de erro indicando sua localização

## Semantico

- Separar entradas, adicionando uma na lista de includes e outra na lista de funcoes, cada funcao possui sua lista de escopo.

## Escopo

> Existem dois tipos de escopo, sendo o primeiro o da funcao e o segundo o escopo da condicional, que so pode existir dentro do escopo da funcao.

- O escopo inicia com `{` e finaliza com `}`.

## Parameters

> O escopo da funcao pode possuir variaveis nos parametros, portanto é necessario avaliar a validar antes de entrar no corpo da funcao.a

## Body (corpo)

> Todo o corpo da funcao é uma lista com informação sobre a linha e conteudo. Estruturas condicionas tambem ficam na lista do corpo, porem de maneira diferente.

## Return

> Realiza a verificação da validade do retorno

## Dificuldades

## Observações

> O arquivo `static.py` contem funcoes e variaveis fixas para serem utilizadas em todo o codigo.

- Criação dos `regexs`
- Revalidacao dos `regexs` para atender o codigo fornecido pelo professor
- Complexidade de validaçoes, sendo necessario criar varios modulos
- Como a estrutura condicional é diferente de um escopo comum, ela não tratada `semanticamente`.

## Transpilar de C para Python

> Pelo tempo 