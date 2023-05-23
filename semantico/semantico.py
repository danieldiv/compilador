import sintatico as s
import re


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


lista_funcoes_int = []
lista_funcoes_float = []
lista_funcoes_double = []
lista_funcoes_char = []
lista_funcoes_void = []


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
    if len(aux) == 2:
        # print(f"aux ---> {aux}")
        aux[1] = aux[1].replace(";", "").replace(")", "").replace("(", "")

        if aux[1].isnumeric():
            return {aux[0]: int(aux[1])}
        elif aux[1].isalpha():
            return {aux[0]: aux[1]}
        elif isFloat(aux[1]):
            return {aux[0]: float(aux[1])}
        else:
            return {aux[0]: [aux[1]]}


def checkCorpo(linha, corpo, params, tipoRetorno):
    x = corpo

    if re.search(s.reg_t1, x):
        match = re.search(s.reg_t1, x)
        aux = match.group().split("=")
        key = aux[0].strip()
        value = aux[1].strip().replace(";", "")

        res = [getParametro(key), value]
    elif re.search(s.reg_return, x):
        match = re.search(s.reg_return, x)
        res = getReturn(match.group())

        if res:
            value = res["return"]

            if isinstance(value, str):
                existe = any(value in p.values() for p in params)
                if not existe:
                    logErro(linha, f"variavel {value} nao declarada")

                for p in params:
                    for tipo, variavel in p.items():
                        if variavel == value:
                            if tipo != tipoRetorno:
                                logErro(linha, f"tipo de retorno invalido")
            elif isinstance(value, int):
                if tipoRetorno != "int":
                    logErro(linha, f"tipo de retorno invalido")
            elif isinstance(value, float):
                if tipoRetorno != "float":
                    logErro(linha, f"tipo de retorno invalido")
            elif isinstance(value, list):
                valores = re.split(r"[+-/*/ ]", value[0])

                for val in valores:
                    if val.isnumeric():
                        if tipoRetorno != "int":
                            logErro(linha, f"tipo de retorno invalido")
                    elif val.isalpha():
                        existe = any(val in p.values() for p in params)
                        if not existe:
                            logErro(linha, f"variavel {val} nao declarada")

                        for p in params:
                            for tipo, variavel in p.items():
                                if variavel == val:
                                    if tipo != tipoRetorno:
                                        logErro(linha, f"tipo de retorno invalido")
                    elif isFloat(val):
                        if tipoRetorno != "float":
                            logErro(linha, f"tipo de retorno invalido")
            return True
        else:
            print("tipo nao identificado")
    return False

    # lista_corpo.append(res)
    #     elif re.search(s.reg_scanf, x):
    #         match = re.search(s.reg_scanf, x)
    #         lista_corpo.append(match.group())
    #     elif re.search(s.reg_printf, x):
    #         match = re.search(s.reg_printf, x)
    #         lista_corpo.append(match.group())
    #     else:
    #         print(f"manteve ----> {x}")
    # return lista_corpo


# todas as key dos dicionarios representam uma linha do codigo
def tratarFuncoes():
    for x in lista_funcoes:
        # print(x)
        findRetorno = False
        expressao = x[0]
        corpo = x[1]

        declaracao = expressao[0]
        parametros = expressao[1]

        for key, value in declaracao.items():
            print(f"funcao ---> {key} {value}")
            if "int" in value:
                value = value.replace("int", "").strip()

                for key, value in parametros.items():
                    params = getParametros(value)
                    print(f"params ---> {params}")

                    for c in corpo:
                        for key, value in c.items():
                            print(f"---> {key} {value}")

                            findRetorno = checkCorpo(key, value, params, "int")
                            if findRetorno:
                                break
                        if findRetorno:
                            break
                    if findRetorno:
                        break
                if findRetorno:
                    break
            if findRetorno:
                break
        # exit()
        print()


#             # lista_funcoes_int.append([aux, getParametros(x[0][1]), getCorpo(x[1])])
#     # for key, value in parametros.items():
#     #     print(key, value)

#     # for c in corpo:
#     #     for key, value in c.items():
#     #         print(key, value)

# if "int" in declaracao:
#     declaracao = declaracao.replace("int", "")
#     print(declaracao)

# if "int " in x[0][0]:
#     aux = x[0][0].replace("int ", "")
#     lista_funcoes_int.append([aux, getParametros(x[0][1]), getCorpo(x[1])])
# if "float " in x[0][0]:
#     aux = x[0][0].replace("float ", "")
#     parametros = getParametros(x[0][1])
#     corpo = getCorpo(x[1], parametros)
#     lista_funcoes_float.append([aux, parametros, corpo])
# elif "double " in x[0][0]:
#     aux = x[0][0].replace("double ", "")
#     lista_funcoes_double.append([aux, getParametros(x[0][1]), getCorpo(x[1])])
# elif "char " in x[0][0]:
#     aux = x[0][0].replace("char ", "")
#     lista_funcoes_char.append([aux, getParametros(x[0][1]), getCorpo(x[1])])
# elif "void " in x[0][0]:
#     aux = x[0][0].replace("void ", "")
#     lista_funcoes_void.append([aux, getParametros(x[0][1]), getCorpo(x[1])])

# for parametros in expressao:
# declaracao = parametros[0]
# parametro = parametros[1]
# print(declaracao)
# print(parametros)
# print(value)
# for key, value in parametro.items():
#     if "float " in value:
#         print("float")
#         print(f"{key} --> {value}")
# aux = value.replace("float ", "")
# print(value)
# aux = x[0][0].replace("float ", "")
# parametros = getParametros(x[0][1])
# corpo = getCorpo(x[1], parametros)
# lista_funcoes_float.append([aux, parametros, corpo])
# else:
#     print(f"{key} --> {value}")

# for value in corpo:
#     for key, value in value.items():
#         print(f"{key} --> {value}")

# finaliza aki

# print()
# printFuncoes()
