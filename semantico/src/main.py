import semantic as sem
import syntatic as sint
import re

# tratar quando for apenas a variavel sem atribuicao
# tratar funcao vazia

# arq = open("../test/original.txt", "r")
# arq = open("../test/code2.txt", "r")
arq = open("../test/código1.txt", "r")

lista = []
linha = 1

for x in arq:
    x = x.strip()
    if len(x) > 0:
        if not re.fullmatch(sint.reg_comment, x):
            if sint.is_valid(linha, x):
                pass
            else:
                print(f"Erro: linha {linha} nao eh valida")
                exit()
    linha = linha + 1

lista = sint.validade

sem.separarEntradas(lista)
sem.tratarFuncoes()