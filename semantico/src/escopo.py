import sintatico as s
import static as st

import re

dados_escopo = []
lista_funcoes = []

escopo_atual = False
definicao = ""
parametros = ""


def initEscopo(linha, expressao):
    global escopo_atual

    if "{" in expressao:
        if not escopo_atual:
            escopo_atual = True
            return True
        else:
            st.logErro(linha, "escopo ja iniciado")
    return False


def endEscopo(linha, expressao):
    global escopo_atual
    global dados_escopo

    if "}" in expressao:
        if escopo_atual:
            lista_funcoes.append([[definicao, parametros], dados_escopo])
            escopo_atual = False
            dados_escopo = []
            return True
        else:
            st.logErro(linha, "} sem escopo")
    return False


def getEscopo(linha, expressao):
    match = re.search(f"{s.reg_funcao.pattern}", expressao)

    if match:
        global definicao
        global parametros

        if initEscopo(linha, expressao):
            expressao = expressao.replace("{", "")
        if endEscopo(linha, expressao):
            expressao = expressao.replace("}", "")

        definicao = re.search(f"{s.reg_tipos.pattern}\w+\s*", expressao).group()
        expressao = expressao.replace(definicao, "")

        if "(" in expressao:
            expressao = expressao.replace("(", "")
        if ")" in expressao:
            expressao = expressao.replace(")", "")

        definicao = definicao.strip()
        definicao = {linha: definicao}

        parametros = expressao.strip()
        parametros = {linha: parametros}

    elif initEscopo(linha, expressao):
        expressao = expressao.replace("{", "")
        if endEscopo(linha, expressao):
            expressao = expressao.replace("}", "")
    elif endEscopo(linha, expressao):
        expressao = expressao.replace("}", "")
    else:
        if escopo_atual:
            dados_escopo.append({linha: expressao})
        else:
            st.logErro(linha, "escopo nao iniciado")
    return True
