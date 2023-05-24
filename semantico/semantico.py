import sintatico as s
import re

INT = "int"
FLOAT = "float"


def logErro(linha, msg):
    print(f"Erro: linha {linha} {msg}")
    exit()


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
lista_escopo = []
reg_f1 = f"{s.reg_tipos.pattern}\w+\s*"


escopo_atual = False
sub_string = ""
parametros = ""


def getFuncoes(linha, expressao):
    match = re.search(reg_f1, expressao)

    global sub_string
    global escopo_atual
    global parametros
    global lista_escopo

    if match and "=" not in expressao:
        sub_string = match.group()
        expressao = expressao.replace(sub_string, "")

        if "{" in expressao:
            escopo_atual = True
            expressao = expressao.replace("{", "")

        if "(" in expressao:
            expressao = expressao.replace("(", "")
        if ")" in expressao:
            expressao = expressao.replace(")", "")

        sub_string = sub_string.strip()
        sub_string = {linha: sub_string}

        parametros = expressao.strip()
        parametros = {linha: parametros}

        return True
    elif "{" in expressao:
        escopo_atual = True
        return True
    elif "}" in expressao:
        if escopo_atual:
            lista_funcoes.append([[sub_string, parametros], lista_escopo])
            escopo_atual = False
            lista_escopo = []
            return True
        else:
            logErro(linha, "}} sem escopo")
    elif escopo_atual:
        lista_escopo.append({linha: expressao})
        return True
    return False


def separarEntradas(lista):
    for x in lista:
        for key, value in x.items():
            if getInclude(key, value):
                continue
            elif getFuncoes(key, value):
                continue
            else:
                print("Sem funcao para tratar: " + value)


def getParametro(parametro):
    parametro = parametro.split()

    if len(parametro) == 2:
        parametro[0] = parametro[0].strip()
        parametro[1] = parametro[1].strip()

        return {parametro[0]: parametro[1]}
    return None


def getParametros(parametros):
    parametros = parametros.split(",")
    lista_parametros = []
    for x in parametros:
        parametro = getParametro(x)
        if parametro:
            lista_parametros.append(parametro)
    return lista_parametros


def isFloat(string):
    try:
        float(string)
        return True
    except:
        return False


def getReturn(corpo):
    aux = corpo.split()
    # print(f"---------------------------> {aux}")
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
    match = re.search(s.reg_return, x)
    res = getReturn(match.group())

    if res:
        value = res["return"]

        if isinstance(value, str):
            existe = any(value in p.values() for p in params)
            if not existe:
                existe = any(value in v.values() for v in lista_variaveis)
                if not existe:
                    logErro(linha, f"variavel {value} nao declarada")

            for p in params:
                for tipo, variavel in p.items():
                    if variavel == value:
                        if tipo != tipoRetorno:
                            logErro(linha, f"tipo de retorno invalido")
        elif isinstance(value, int):
            if tipoRetorno != INT:
                logErro(linha, f"tipo de retorno invalido")
        elif isinstance(value, float):
            if tipoRetorno != FLOAT:
                logErro(linha, f"tipo de retorno invalido")
        elif isinstance(value, list):
            valores = re.split(r"[+-/*/ ]", value[0])

            for val in valores:
                if val.isnumeric():
                    if tipoRetorno != INT:
                        logErro(linha, f"tipo de retorno invalido")
                elif val.isalpha():
                    existe = any(val in p.values() for p in params)
                    if not existe:
                        existe = any(value in v.values() for v in lista_variaveis)
                        if not existe:
                            logErro(linha, f"variavel {value} nao declarada")

                    for p in params:
                        for tipo, variavel in p.items():
                            if variavel == val:
                                if tipo != tipoRetorno:
                                    logErro(linha, f"tipo de retorno invalido")
                elif isFloat(val):
                    if tipoRetorno != FLOAT:
                        logErro(linha, f"tipo de retorno invalido")
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
    logErro(linha, f"funcao {nome_funcao} nao declarada")


def check_variavel(linha, params, x):
    match = re.search(s.reg_t1, x)
    aux = match.group().split("=")
    key = aux[0].strip()
    value = aux[1].strip().replace(";", "")

    # posicao 0 = variavel com tipo, posicao 1 = valor
    res = [getParametro(key), value]

    for key, var in res[0].items():
        existe = any(var in p.values() for p in params)
        if existe:
            logErro(linha, f"variavel {var} ja foi declarada")
        else:
            existe = any(var in v.values() for v in lista_variaveis)
            if existe:
                logErro(linha, f"variavel {var} ja foi declarada")

        value = value.strip()
        print(value)

        if value.isnumeric():
            if INT != key:
                logErro(linha, f"tipo de variavel invalido")
        elif value.isalpha():
            existe = any(value in p.values() for p in params)
            if not existe:
                existe = any(value in v.values() for v in lista_variaveis)
                if not existe:
                    logErro(linha, f"variavel {value} nao foi declarada")
        elif isFloat(value):
            pass
        else:
            reg = r"[\w]+"
            match = re.search(reg, value)
            if match:
                nome_funcao = match.group()

                check_nome_funcao(linha, key, nome_funcao)

                print()
                value = value.replace(match.group(), "")
                print(value)
            # print(f"{value} sem tratamento")

    lista_variaveis.append(res[0])


def check_variavel_existente(linha, params, val, tipoRetorno):
    # verifica o tipo com relacao aos parametros
    if len(params) != 0:
        for p in params:
            for tipo, variavel in p.items():
                if variavel == val:
                    # se o tipo nao existir nos parametros, verifica nas variaveis
                    if tipo != tipoRetorno:
                        for v in lista_variaveis:
                            for tipo, variavel in v.items():
                                if variavel == val:
                                    # se o tipo nao existir nas variaveis, erro
                                    if tipo != tipoRetorno:
                                        logErro(linha, f"tipo de variavel invalido")
    else:
        for v in lista_variaveis:
            for tipo, variavel in v.items():
                if variavel == val:
                    # se o tipo nao existir nas variaveis, erro
                    if tipo != tipoRetorno:
                        logErro(linha, f"tipo de variavel invalido")


def checkCorpo(linha, corpo, params, tipoRetorno):
    x = corpo

    if re.search(s.reg_t1, x):
        check_variavel(linha, params, x)
    elif re.search(s.reg_return, x):
        if check_retorno(x, linha, params, tipoRetorno):
            return True
    elif re.search(s.reg_scanf, x):
        x = (
            x.replace("scanf", "")
            .replace(";", "")
            .replace("(", "")
            .replace(")", "")
            .strip()
        )
        # aux = x.split(",")
        # for val in aux:
        #     val = val.strip()
        #     if '"' in val:
        #         pass
        #     else:
        #         if val.isnumeric():
        #             if "%d" not in aux[0]:
        #                 logErro(linha, f"tipo de variavel invalido")
        #         elif val.isalpha():
        #             if isinstance(val, str):
        #                 existe = any(val in p.values() for p in params)
        #                 if not existe:
        #                     existe = any(val in v.values() for v in lista_variaveis)
        #                     if not existe:
        #                         logErro(linha, f"variavel {val} nao declarada")
        #                 if "%d" in aux[0]:
        #                     check_variavel_existente(linha, params, val, INT)
        #                 elif "%f" in aux[0]:
        #                     check_variavel_existente(linha, params, val, FLOAT)
        #                 else:
        #                     logErro(linha, f"tipo de variavel invalido")

        #         elif isFloat(val):
        #             print("float")
    elif re.search(s.reg_printf, x):
        x = (
            x.replace("printf", "")
            .replace(";", "")
            .replace("(", "")
            .replace(")", "")
            .strip()
        )
        aux = x.split(",")
        for val in aux:
            val = val.strip()
            if '"' in val:
                pass
            else:
                if val.isnumeric():
                    if "%d" not in aux[0]:
                        logErro(linha, f"tipo de variavel invalido")
                elif val.isalpha():
                    if isinstance(val, str):
                        existe = any(val in p.values() for p in params)
                        if not existe:
                            existe = any(val in v.values() for v in lista_variaveis)
                            if not existe:
                                logErro(linha, f"variavel {val} nao declarada")
                        if "%d" in aux[0]:
                            check_variavel_existente(linha, params, val, INT)
                        elif "%f" in aux[0]:
                            check_variavel_existente(linha, params, val, FLOAT)
                        else:
                            logErro(linha, f"tipo de variavel invalido")

                elif isFloat(val):
                    print("float")
    else:
        print(f"manteve ----> {x}")
    # print()
    return False


def check_funcao(value, corpo, parametros, tipo):
    value = value.replace(tipo, "").strip()

    for key, value in parametros.items():
        params = getParametros(value)
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
            lista_nome_funcoes.append({aux[0]: aux[1]})

            if INT in value:
                check_funcao(value, corpo, parametros, INT)
            elif FLOAT in value:
                check_funcao(value, corpo, parametros, FLOAT)

        print("\nVARIAVEIS DECLARADAS")
        for v in lista_variaveis:
            for key, value in v.items():
                print(f"--> {key} {value}")
        print()

    print("SEMANTICO")
    for x in lista_nome_funcoes:
        print(x)
