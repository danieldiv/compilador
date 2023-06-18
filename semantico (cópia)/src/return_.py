import syntatic as sint
import static as st

import re


# verifica se variavel nao foi declarada
def test_variavel_inesistente(variavel, params, linha, lista_variaveis):
    existe = any(variavel in p.values() for p in params)
    if not existe:
        existe = any(variavel in v.values() for v in lista_variaveis)
        if not existe:
            st.logErro(linha, f"variavel {variavel} nao foi declarada")


def getReturn(corpo):
    aux = corpo.split()
    if len(aux) == 2:
        aux[1] = aux[1].replace(";", "").replace(")", "").replace("(", "")

        if aux[1].isnumeric():
            return {aux[0]: int(aux[1])}
        elif aux[1].isalpha():
            return {aux[0]: aux[1]}
        elif st.isFloat(aux[1]):
            return {aux[0]: float(aux[1])}
        else:
            return {aux[0]: [aux[1]]}


def check_retorno(x, linha, params, tipoRetorno, lista_variaveis):
    match = re.match(sint.reg_return, x)
    res = getReturn(match.group())

    if res:
        value = res["return"]

        if isinstance(value, str):
            test_variavel_inesistente(value, params, linha, lista_variaveis)

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
                    test_variavel_inesistente(val, params, linha, lista_variaveis)

                    for p in params:
                        for tipo, variavel in p.items():
                            if variavel == val:
                                if tipo != tipoRetorno:
                                    st.logErro(linha, f"tipo de retorno invalido")
                elif st.isFloat(val):
                    if tipoRetorno != st.FLOAT:
                        st.logErro(linha, f"tipo de retorno invalido")
        return True
    else:
        print(f"tipo nao identificado {x}")
    return False
