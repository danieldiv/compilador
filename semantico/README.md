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