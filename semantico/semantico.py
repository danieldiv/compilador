import sintatico as s
import re

arq = open("files/code.txt", "r")
lista = []
key = 1

for x in arq:
    mapa = {}
    x = x.strip()
    if len(x) > 0:
        if not re.fullmatch(s.reg_comment, x):
            if s.is_valid(x):
                mapa[key] = x
                lista.append(mapa)
            else:
                print(f"Erro: linha {key} não é valida")
                exit()
        else:
            pass
            # print(f"comentario --> {x}")
    key += 1


lista_include = []

# key = 1
# for x in lista:
#     print(x)
# exit()


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
            print(f"Erro: linha {linha} }} sem escopo")
            exit()
    elif escopo_atual:
        lista_escopo.append({linha: expressao})
        return True
    return False


for x in lista:
    for key, value in x.items():
        if getInclude(key, value):
            continue
        elif getFuncoes(key, value):
            continue
        else:
            print("Sem funcao para tratar: " + value)


# for x in lista_include:
#     print(f"include --> {x}")

# for x in lista_funcoes:
#     for y in x:
#         print(y)
# exit()
lista_funcoes_int = []
lista_funcoes_float = []
lista_funcoes_double = []
lista_funcoes_char = []
lista_funcoes_void = []

# f -> funcao
# p -> parametro
# c -> corpo


def printFuncao(lista, name):
    print(f"FUNCOES {name}:")
    for x in lista:
        print(f"f --> {x[0]}")
        for y in x[1]:
            print(f"p --> {y}")
        for z in x[2]:
            print(f"c --> {z}")
        print()


def printFuncoes():
    if len(lista_funcoes_int) > 0:
        printFuncao(lista_funcoes_int, "INT")

    if len(lista_funcoes_float) > 0:
        printFuncao(lista_funcoes_float, "FLOAT")

    if len(lista_funcoes_double) > 0:
        printFuncao(lista_funcoes_double, "DOUBLE")

    if len(lista_funcoes_char) > 0:
        printFuncao(lista_funcoes_char, "CHAR")

    if len(lista_funcoes_void) > 0:
        printFuncao(lista_funcoes_void, "VOID")


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
        aux[1] = aux[1].replace(";", "").replace(")", "").replace("(", "")

        if aux[1].isnumeric():
            return {aux[0]: int(aux[1])}
        elif aux[1].isalpha():
            return {aux[0]: aux[1]}
        elif isFloat(aux[1]):
            return {aux[0]: float(aux[1])}


def getCorpo(corpo, parametros):
    lista_corpo = []
    for x in corpo:
        if re.search(s.reg_t1, x):
            match = re.search(s.reg_t1, x)
            aux = match.group().split("=")
            key = aux[0].strip()
            value = aux[1].strip().replace(";", "")

            res = [getParametro(key), value]
            lista_corpo.append(res)
        elif re.search(s.reg_return, x):
            match = re.search(s.reg_return, x)
            res = getReturn(match.group())
            if res:
                value = res["return"]
                if isinstance(value, str):
                    existe = any(
                        value in parametro.values() for parametro in parametros
                    )
                    if not existe:
                        print(f"Erro: variavel {value} não declarada")
                        exit()

            lista_corpo.append(res)
        elif re.search(s.reg_scanf, x):
            match = re.search(s.reg_scanf, x)
            lista_corpo.append(match.group())
        elif re.search(s.reg_printf, x):
            match = re.search(s.reg_printf, x)
            lista_corpo.append(match.group())
        else:
            print(f"manteve ----> {x}")
    return lista_corpo


for x in lista_funcoes:
    expressao = x[0]
    corpo = x[1]

    # comeca aki
    
    declaracao = expressao[0]
    parametros = expressao[1]
    
    print(expressao)
    print(declaracao)
    print(parametros)
    # print(corpo)

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

# print()
printFuncoes()
