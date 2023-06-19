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


def printFuncoes():
    print("FUNCOES")
    for corpo in lista_funcoes:
        for c in corpo:
            for valores in c:
                if not isinstance(valores, list):
                    for key, value in valores.items():
                        st.printLine(key, value)
                else:
                    condicao = valores[0]
                    corpo_condicao = valores[1]
                    st.printMessage(condicao)

                    for c in corpo_condicao:
                        for key, value in c.items():
                            st.logWarning(
                                key, f"sem tratamento para condicional {value}"
                            )
        print()
    exit()


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
    st.printTitle("INCLUDES")
    for x in lista_include:
        for key, value in x.items():
            st.printLine(key, value)
    print()
    # printFuncoes()


lista_variaveis = []


def check_funcao(corpo, parametros, tipo):
    for key, value in parametros.items():
        params = par.getParametros(value)
        print(f"{st.CYAN}params {st.GREEN}-->{st.RESET} {params}")

        for c in corpo:
            if not isinstance(c, list):
                for key, value in c.items():
                    st.printLine(key, value)
                    bd.lista_variaveis = lista_variaveis
                    bd.lista_nome_funcoes = lista_nome_funcoes

                    if bd.checkCorpo(key, value, params, tipo):
                        return
            else:
                condicao = c[0]
                # corpo_condicao = c[1]
                for key, value in condicao[0].items():
                    st.logWarning(key, f"sem tratamento para condicional {value}")


# todas as key dos dicionarios representam uma linha do codigo
def tratarFuncoes():
    for x in lista_funcoes:
        expressao = x[0]
        corpo = x[1]

        global lista_variaveis
        lista_variaveis = []

        declaracao = expressao[0]
        parametros = expressao[1]

        if st.CONDICIONAL not in declaracao and st.ELSE not in declaracao:
            for key, value in declaracao.items():
                print(f"{st.CYAN}funcao {st.GREEN}-->{st.RESET} {key} {value}")
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

                if len(lista_variaveis) > 0:
                    st.printTitle("\nVARIAVEIS DECLARADAS")
                    for v in lista_variaveis:
                        for key, value in v.items():
                            st.printLine(key, value)
                print()
        else:
            st.printWarning("funcao com condicional")
            print(f"{declaracao}")
            print(f"{parametros}")
            print(f"{corpo}")
            print()

    st.printTitle("SEMANTICO")
    for x in lista_nome_funcoes:
        print(x)
