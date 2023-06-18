# valida o corpo da funcao

import syntatic as sint
import static as st
import parameters as par
import return_ as ret

import re

lista_variaveis = []
lista_nome_funcoes = []


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


# verifica se valor da variavel eh valido para o tipo declarado
def check_tipo_variavel(linha, params, val, tipoRetorno):
    if len(params) != 0:
        res = check_variavel_in_params(params, val, tipoRetorno)
        if not res:
            check_variavel_in_lista(linha, val, tipoRetorno)
    else:
        check_variavel_in_lista(linha, val, tipoRetorno)


# verifica se a varivel ja foi declarada
def test_variavel_existencia(variavel, params, linha):
    existe = any(variavel in p.values() for p in params)
    if existe:
        st.logErro(linha, f"variavel {variavel} ja foi declarada")
    else:
        existe = any(variavel in v.values() for v in lista_variaveis)
        if existe:
            st.logErro(linha, f"variavel {variavel} ja foi declarada")


# verifica se variavel nao foi declarada
def test_variavel_inesistente(variavel, params, linha):
    existe = any(variavel in p.values() for p in params)
    if not existe:
        existe = any(variavel in v.values() for v in lista_variaveis)
        if not existe:
            st.logErro(linha, f"variavel {variavel} nao foi declarada")


# verifica se variavel existe para ser utilizada e se o tipo de retorno eh valido
def check_variavel_existente(linha, params, val, esq):
    test_variavel_inesistente(val, params, linha)

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


# verifica se o nome da funcao foi declarado
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
        test_variavel_existencia(variavel, params, linha)
        lista_variaveis.append({tipo: variavel})


def check_variavel(linha, params, x):
    match = re.search(sint.reg_t1, x)
    aux = match.group().split("=")

    key = aux[0].strip()
    value = aux[1].strip().replace(";", "")

    # posicao 0 = variavel com tipo, posicao 1 = valor
    res = [par.getParametro(key), value]

    for key, variavel in res[0].items():
        test_variavel_existencia(variavel, params, linha)

        value = value.strip()

        if value.isnumeric():
            if st.INT != key:
                st.logErro(linha, f"tipo de variavel invalido")
        elif value.isalpha():
            test_variavel_inesistente(value, params, linha)
        elif st.isFloat(value):
            pass
        else:
            reg = r"[\w]+"
            match = re.search(reg, value)
            if match:
                nome_funcao = match.group()
                check_nome_funcao(linha, key, nome_funcao)
                value = value.replace(match.group(), "")

    lista_variaveis.append(res[0])


def checkCorpo(linha, corpo, params, tipoRetorno):
    x = corpo

    if re.search(sint.reg_t0, x):
        check_variavel_sem_atribuicao(linha, params, x)
    elif re.search(sint.reg_t1, x):
        check_variavel(linha, params, x)
    elif re.search(sint.reg_return, x):
        if ret.check_retorno(x, linha, params, tipoRetorno, lista_variaveis):
            return True
    elif re.search(sint.reg_scanf, x):
        res = getReadWrite("scanf", x)
        if "&" in res[1]:
            res[1] = res[1].replace("&", "")
            check_variavel_existente(linha, params, res[1], res[0])
    elif re.search(sint.reg_printf, x):
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
