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
