import sintatico as s

import static as st
import parametros as p
import escopo as e

import re


lista_include = []


def getInclude(linha, expressao):
    if "#include" in expressao:
        expressao = expressao.split()

        if len(expressao) > 1:
            lista_include.append(expressao[1])
        else:
            lista_include.append(expressao[0].replace("#include", ""))
        return True
    return False


lista_funcoes = []
lista_nome_funcoes = []


def separarEntradas(lista):
    global lista_funcoes
    for x in lista:
        for key, value in x.items():
            if getInclude(key, value):
                continue
            elif e.getEscopo(key, value):
                continue
            else:
                st.logErro(key, "sem funcao para tratar: " + value)
    lista_funcoes = e.lista_funcoes


# def getParametro(parametro):
#     parametro = parametro.split()

#     if len(parametro) == 2:
#         parametro[0] = parametro[0].strip()
#         parametro[1] = parametro[1].strip()

#         return {parametro[0]: parametro[1]}
#     return None


# def getParametros(parametros):
#     parametros = parametros.split(",")
#     lista_parametros = []
#     for x in parametros:
#         parametro = getParametro(x)
#         if parametro:
#             lista_parametros.append(parametro)
#     return lista_parametros


def isFloat(string):
    try:
        float(string)
        return True
    except:
        return False


def getReturn(corpo):
    aux = corpo.split()
    if len(aux) == 2:
        aux[1] = aux[1].replace(";", "").replace(")", "").replace("(", "")

        if aux[1].isnumeric():
            return {aux[0]: int(aux[1])}
        elif aux[1].isalpha():
            return {aux[0]: aux[1]}
        elif isFloat(aux[1]):
            return {aux[0]: float(aux[1])}
        else:
            return {aux[0]: [aux[1]]}


def check_retorno(x, linha, params, tipoRetorno):
    match = re.match(s.reg_return, x)
    res = getReturn(match.group())

    if res:
        value = res["return"]

        if isinstance(value, str):
            existe = any(value in p.values() for p in params)
            if not existe:
                existe = any(value in v.values() for v in lista_variaveis)
                if not existe:
                    st.logErro(linha, f"variavel {value} nao declarada")

            for p in params:
                for tipo, variavel in p.items():
                    if variavel == value:
                        if tipo != tipoRetorno:
                            st.logErro(linha, f"tipo de retorno invalido")
        elif isinstance(value, int):
            if tipoRetorno != st.INT:
                st.logErro(linha, f"tipo de retorno invalido")
        elif isinstance(value, float):
            if tipoRetorno != st.FLOAT:
                st.logErro(linha, f"tipo de retorno invalido")
        elif isinstance(value, list):
            valores = re.split(r"[+-/*/ ]", value[0])

            for val in valores:
                if val.isnumeric():
                    if tipoRetorno != st.INT:
                        st.logErro(linha, f"tipo de retorno invalido")
                elif val.isalpha():
                    existe = any(val in p.values() for p in params)
                    if not existe:
                        existe = any(value in v.values() for v in lista_variaveis)
                        if not existe:
                            st.logErro(linha, f"variavel {value} nao declarada")

                    for p in params:
                        for tipo, variavel in p.items():
                            if variavel == val:
                                if tipo != tipoRetorno:
                                    st.logErro(linha, f"tipo de retorno invalido")
                elif isFloat(val):
                    if tipoRetorno != st.FLOAT:
                        st.logErro(linha, f"tipo de retorno invalido")
        return True
    else:
        print(f"tipo nao identificado {x}")
    return False


lista_variaveis = []


def check_nome_funcao(linha, tipo_funcao, nome_funcao):
    for funcoes in lista_nome_funcoes:
        for tipo, nome in funcoes.items():
            if nome_funcao == nome:
                if tipo == tipo_funcao:
                    return
    st.logErro(linha, f"funcao {nome_funcao} nao declarada")


def check_variavel_sem_atribuicao(linha, params, x):
    x = x.replace(";", "").strip()
    x = x.replace(", ", ",").strip()
    x = x.split()

    tipo = x[0].strip()
    variaveis = x[1].split(",")

    for variavel in variaveis:
        existe = any(variavel in p.values() for p in params)
        if existe:
            st.logErro(linha, f"variavel {variavel} ja foi declarada")
        else:
            existe = any(variavel in v.values() for v in lista_variaveis)
            if existe:
                st.logErro(linha, f"variavel {variavel} ja foi declarada")

        lista_variaveis.append({tipo: variavel})


def check_variavel(linha, params, x):
    match = re.search(s.reg_t1, x)
    aux = match.group().split("=")

    key = aux[0].strip()
    value = aux[1].strip().replace(";", "")

    # posicao 0 = variavel com tipo, posicao 1 = valor
    res = [p.getParametro(key), value]

    for key, var in res[0].items():
        existe = any(var in p.values() for p in params)
        if existe:
            st.logErro(linha, f"variavel {var} ja foi declarada")
        else:
            existe = any(var in v.values() for v in lista_variaveis)
            if existe:
                st.logErro(linha, f"variavel {var} ja foi declarada")

        value = value.strip()

        if value.isnumeric():
            if st.INT != key:
                st.logErro(linha, f"tipo de variavel invalido")
        elif value.isalpha():
            existe = any(value in p.values() for p in params)
            if not existe:
                existe = any(value in v.values() for v in lista_variaveis)
                if not existe:
                    st.logErro(linha, f"variavel {value} nao foi declarada")
        elif isFloat(value):
            pass
        else:
            reg = r"[\w]+"
            match = re.search(reg, value)
            if match:
                nome_funcao = match.group()
                check_nome_funcao(linha, key, nome_funcao)
                value = value.replace(match.group(), "")

    lista_variaveis.append(res[0])


def check_variavel_in_lista(linha, val, tipoRetorno):
    for v in lista_variaveis:
        for tipo, variavel in v.items():
            if variavel == val:
                if tipo != tipoRetorno:
                    st.logErro(linha, f"tipo de variavel invalido")


def check_variavel_in_params(params, val, tipoRetorno):
    for p in params:
        for tipo, variavel in p.items():
            if variavel == val:
                if tipo == tipoRetorno:
                    return True
    return False


def check_tipo_variavel(linha, params, val, tipoRetorno):
    if len(params) != 0:
        res = check_variavel_in_params(params, val, tipoRetorno)
        if not res:
            check_variavel_in_lista(linha, val, tipoRetorno)
    else:
        check_variavel_in_lista(linha, val, tipoRetorno)


def check_variavel_existente(linha, params, val, esq):
    existe = any(val in p.values() for p in params)
    if not existe:
        existe = any(val in v.values() for v in lista_variaveis)
        if not existe:
            st.logErro(linha, f"variavel {val} nao declarada")
    if "%d" in esq:
        check_tipo_variavel(linha, params, val, st.INT)
    elif "%i" in esq:
        check_tipo_variavel(linha, params, val, st.INT)
    elif "%c" in esq:
        check_tipo_variavel(linha, params, val, st.CHAR)
    elif "%f" in esq:
        check_tipo_variavel(linha, params, val, st.FLOAT)
    elif "%lf" in esq:
        check_tipo_variavel(linha, params, val, st.DOUBLE)
    else:
        st.logErro(linha, f"tipo de variavel invalido")


def getReadWrite(value, x):
    x = (
        x.replace(f"{value}", "")
        .replace(";", "")
        .replace("(", "")
        .replace(")", "")
        .strip()
    )
    aux = x.split(",")
    if len(aux) == 1:
        return [aux[0].strip(), ""]
    return [aux[0].strip(), aux[1].strip()]


def checkCorpo(linha, corpo, params, tipoRetorno):
    x = corpo

    if re.search(s.reg_t0, x):
        check_variavel_sem_atribuicao(linha, params, x)
    elif re.search(s.reg_t1, x):
        check_variavel(linha, params, x)
    elif re.search(s.reg_return, x):
        if check_retorno(x, linha, params, tipoRetorno):
            return True
    elif re.search(s.reg_scanf, x):
        res = getReadWrite("scanf", x)
        if "&" in res[1]:
            res[1] = res[1].replace("&", "")
            check_variavel_existente(linha, params, res[1], res[0])
    elif re.search(s.reg_printf, x):
        res = getReadWrite("printf", x)
        if res[1].isnumeric():
            if "%d" not in res[0]:
                st.logErro(linha, f"tipo de variavel invalido")
        elif res[1].isalpha():
            if isinstance(res[1], str):
                check_variavel_existente(linha, params, res[1], res[0])
    else:
        print(f"manteve ----> {x}")
    return False


def check_funcao(corpo, parametros, tipo):
    for key, value in parametros.items():
        params = p.getParametros(value)
        print(f"params    ---> {params}")

        for c in corpo:
            for key, value in c.items():
                print(f"---> {key} {value}")

                if checkCorpo(key, value, params, tipo):
                    return


# todas as key dos dicionarios representam uma linha do codigo
def tratarFuncoes():
    for x in lista_funcoes:
        expressao = x[0]
        corpo = x[1]

        global lista_variaveis
        lista_variaveis = []

        declaracao = expressao[0]
        parametros = expressao[1]

        for key, value in declaracao.items():
            print(f"funcao    ---> {key} {value}")
            aux = value.split()

            exist = any(aux[1] in p.values() for p in lista_nome_funcoes)
            if exist:
                st.logErro(key, f"funcao {aux[1]} ja foi declarada")

            lista_nome_funcoes.append({aux[0]: aux[1]})

            if st.INT in value:
                check_funcao(corpo, parametros, st.INT)
            elif st.FLOAT in value:
                check_funcao(corpo, parametros, st.FLOAT)
            elif st.VOID in value:
                check_funcao(corpo, parametros, st.VOID)
            else:
                print(f"tipo nao identificado: {value}")

            print("\nVARIAVEIS DECLARADAS")
            for v in lista_variaveis:
                for key, value in v.items():
                    print(f"--> {key} {value}")
            print()

    print("SEMANTICO")
    for x in lista_nome_funcoes:
        print(x)
