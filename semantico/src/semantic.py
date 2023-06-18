import static as st
import parameters as par
import escope as esc
import body as bd

lista_include = []
lista_funcoes = []
lista_nome_funcoes = []


def getInclude(linha, expressao):
    if "#include" in expressao:
        expressao = expressao.split()

        if len(expressao) > 1:
            lista_include.append({linha: expressao[1]})
        else:
            lista_include.append({linha: expressao[0].replace("#include", "")})
        return True
    return False


def separarEntradas(lista):
    global lista_funcoes
    for x in lista:
        for key, value in x.items():
            if getInclude(key, value):
                continue
            elif esc.getEscopo(key, value):
                continue
            else:
                st.logErro(key, "sem funcao para tratar: " + value)
    lista_funcoes = esc.lista_funcoes

    print("INCLUDES")
    for x in lista_include:
        for key, value in x.items():
            print(f"{st.GREEN}-->{st.RESET} {key} {value}")
    print()


lista_variaveis = []


def check_funcao(corpo, parametros, tipo):
    for key, value in parametros.items():
        params = par.getParametros(value)
        print(f"params    {st.GREEN}-->{st.RESET} {params}")

        for c in corpo:
            for key, value in c.items():
                print(f"{st.GREEN}-->{st.RESET} {key} {value}")

                bd.lista_variaveis = lista_variaveis
                bd.lista_nome_funcoes = lista_nome_funcoes

                if bd.checkCorpo(key, value, params, tipo):
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
            print(f"funcao    {st.GREEN}-->{st.RESET} {key} {value}")
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
                    print(f"{st.GREEN}-->{st.RESET} {key} {value}")
            print()

    print("SEMANTICO")
    for x in lista_nome_funcoes:
        print(x)
