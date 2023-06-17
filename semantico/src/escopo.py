import sintatico as s
import static as st

import re

dados_escopo = []
lista_funcoes = []
# funcao = []

escopo_atual = False
definicao = ""
parametros = ""


def initEscopo(linha, expressao):
    global escopo_atual

    if "{" in expressao:
        if not escopo_atual:
            # print("init escopo")
            escopo_atual = True
            return True
        else:
            st.logErro(linha, "escopo ja iniciado")
    return False


def endEscopo(linha, expressao):
    global escopo_atual
    global dados_escopo
    # global funcao

    if "}" in expressao:
        if escopo_atual:
            # print("end escopo")
            lista_funcoes.append([[definicao, parametros], dados_escopo])
            escopo_atual = False
            dados_escopo = []
            return True
        else:
            st.logErro(linha, "} sem escopo")
    return False


def getEscopo(linha, expressao):
    match = re.search(f"{s.reg_funcao.pattern}", expressao)
    # match = re.search(f"{s.reg_tipos.pattern}\w+\s*", expressao)

    if match:
        global definicao
        global parametros

        # print(f"fun --->: {expressao}")

        if initEscopo(linha, expressao):
            expressao = expressao.replace("{", "")
        if endEscopo(linha, expressao):
            expressao = expressao.replace("}", "")

        # definicao = match.group()
        definicao = re.search(f"{s.reg_tipos.pattern}\w+\s*", expressao).group()
        # print(re.search(f"{s.reg_tipos.pattern}\w+\s*", expressao).group())
        expressao = expressao.replace(definicao, "")

        if "(" in expressao:
            expressao = expressao.replace("(", "")
        if ")" in expressao:
            expressao = expressao.replace(")", "")

        definicao = definicao.strip()
        definicao = {linha: definicao}

        parametros = expressao.strip()
        parametros = {linha: parametros}

        # print(f"d --->: {definicao}")
        # print(f"p --->: {expressao}")
        # print()

    elif initEscopo(linha, expressao):
        expressao = expressao.replace("{", "")
        if endEscopo(linha, expressao):
            expressao = expressao.replace("}", "")
    elif endEscopo(linha, expressao):
        expressao = expressao.replace("}", "")
    else:
        if escopo_atual:
            # print(f"esc --->: {expressao}")
            dados_escopo.append({linha: expressao})
        else:
            st.logErro(linha, "escopo nao iniciado")
    return True

    # global sub_string
    # global escopo_atual
    # global parametros
    # global lista_escopo

    # if match and "=" not in expressao:
    #     print(f"funcao: {expressao}")
    #     sub_string = match.group()
    #     expressao = expressao.replace(sub_string, "")

    #     if "{" in expressao:
    #         escopo_atual = True
    #         expressao = expressao.replace("{", "")

    #     if "(" in expressao:
    #         expressao = expressao.replace("(", "")
    #     if ")" in expressao:
    #         expressao = expressao.replace(")", "")

    #     sub_string = sub_string.strip()
    #     sub_string = {linha: sub_string}

    #     parametros = expressao.strip()
    #     parametros = {linha: parametros}

    #     return True
    # elif "{" in expressao:
    #     escopo_atual = True
    #     return True
    # elif "}" in expressao:
    #     if escopo_atual:
    #         # retornar lista lista_funcoes
    #         # lista_funcoes.append([[sub_string, parametros], lista_escopo])
    #         escopo_atual = False
    #         lista_escopo = []
    #         return True
    #     else:
    #         st.logErro(linha, "}} sem escopo")
    # elif escopo_atual:
    #     # retornar lista lista_escopo
    #     # lista_escopo.append({linha: expressao})
    #     return True
    # return False
