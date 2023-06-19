# separa o codigo em escopos

import syntatic as s
import static as st

import re

dados_escopo_funcao = []
dados_escopo_condicional = []

lista_funcoes = []
lista_condicional = []

escopo_funcao = False
escopo_condicional = False
condicional = False
else_condicional = False

definicao = ""
parametros = ""
comparacao = ""


def initEscopo(linha, expressao):
    global escopo_funcao

    if "{" in expressao:
        if not escopo_funcao:
            escopo_funcao = True
            return True
        else:
            st.logErro(linha, "escopo funcao ja iniciado")
    return False


def initEscopoCondicional(linha, expressao):
    global escopo_condicional

    if "{" in expressao:
        if not escopo_condicional and escopo_funcao:
            escopo_condicional = True
            return True
        else:
            st.logErro(linha, "escopo condicional ja iniciado")
    return False


def endEscopo(linha, expressao):
    global escopo_funcao
    global dados_escopo_funcao

    if "}" in expressao:
        if escopo_funcao:
            lista_funcoes.append([[definicao, parametros], dados_escopo_funcao])
            escopo_funcao = False
            dados_escopo_funcao = []
            return True
        else:
            st.logErro(linha, "} sem escopo")
    return False


def endEscopoCondicional(linha, expressao):
    global escopo_condicional
    global dados_escopo_condicional
    global condicional

    if "}" in expressao:
        if escopo_condicional and escopo_funcao:
            dados_escopo_funcao.append([comparacao, dados_escopo_condicional])
            escopo_condicional = False
            condicional = False
            dados_escopo_condicional = []
            return True
        else:
            st.logErro(linha, "} sem escopo")
    return False


def limparFuncao(linha, expressao):
    global definicao
    global parametros

    if initEscopo(linha, expressao):
        expressao = expressao.replace("{", "")
    if endEscopo(linha, expressao):
        expressao = expressao.replace("}", "")

    definicao = re.search(f"{s.reg_tipos}\w+\s*", expressao).group()
    expressao = expressao.replace(definicao, "")

    if "(" in expressao:
        expressao = expressao.replace("(", "")
    if ")" in expressao:
        expressao = expressao.replace(")", "")

    definicao = definicao.strip()
    definicao = {linha: definicao}

    parametros = expressao.strip()
    parametros = {linha: parametros}


def limparCondicional(linha, expressao):
    global condicional
    global comparacao

    condicional = True

    if initEscopoCondicional(linha, expressao):
        expressao = expressao.replace("{", "")
    if endEscopoCondicional(linha, expressao):
        expressao = expressao.replace("}", "")

    if "(" in expressao:
        expressao = expressao.replace("(", "")
    if ")" in expressao:
        expressao = expressao.replace(")", "")

    if st.CONDICIONAL in expressao:
        expressao = expressao.replace(st.CONDICIONAL, "").strip()
        condicional = re.search(f"{s.reg_comparacao}", expressao).group()
        expressao = expressao.replace(condicional, "")
        valores = expressao.split()
        comparacao = {
            linha: [valores[0].strip(), condicional.strip(), valores[1].strip()]
        }
        comparacao = [{linha: st.CONDICIONAL}, comparacao]
    elif st.ELSE in expressao:
        comparacao = {linha: ""}
        comparacao = [{linha: st.ELSE}, comparacao]
    else:
        st.logErro(linha, "escopo condicional invalido")


def adicionarDadosFuncao(linha, expressao):
    if initEscopo(linha, expressao):
        expressao = expressao.replace("{", "")
        if endEscopo(linha, expressao):
            expressao = expressao.replace("}", "")
    elif endEscopo(linha, expressao):
        expressao = expressao.replace("}", "")
    else:
        if escopo_funcao:
            dados_escopo_funcao.append({linha: expressao})
        else:
            st.logErro(linha, "escopo funcao nao iniciado")


def adicionarDadosCondicional(linha, expressao):
    if initEscopoCondicional(linha, expressao):
        expressao = expressao.replace("{", "")
        if endEscopoCondicional(linha, expressao):
            expressao = expressao.replace("}", "")
    elif endEscopoCondicional(linha, expressao):
        expressao = expressao.replace("}", "")
    else:
        if escopo_condicional:
            dados_escopo_condicional.append({linha: expressao})
        else:
            st.logErro(linha, "escopo condicional nao iniciado")


def getEscopo(linha, expressao):
    match = re.search(f"{s.reg_funcao.pattern}", expressao)

    if match:
        limparFuncao(linha, expressao)
    elif re.search(f"{s.reg_condicional.pattern}", expressao):
        limparCondicional(linha, expressao)
    elif condicional and not else_condicional:
        adicionarDadosCondicional(linha, expressao)
    else:
        adicionarDadosFuncao(linha, expressao)
    return True
