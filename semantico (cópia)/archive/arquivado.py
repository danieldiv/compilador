# def printFuncao(lista, name):
#     print(f"FUNCOES {name}:")
#     for x in lista:
#         print(f"f {st.GREEN}-->{st.RESET} {x[0]}")  # funcao
#         for y in x[1]:
#             print(f"p {st.GREEN}-->{st.RESET} {y}")  # parametro
#         for z in x[2]:
#             print(f"c {st.GREEN}-->{st.RESET} {z}")  # corpo
#         print()


# def printFuncoes():
#     if len(lista_funcoes_int) > 0:
#         printFuncao(lista_funcoes_int, "INT")

#     if len(lista_funcoes_float) > 0:
#         printFuncao(lista_funcoes_float, "FLOAT")

#     if len(lista_funcoes_double) > 0:
#         printFuncao(lista_funcoes_double, "DOUBLE")

#     if len(lista_funcoes_char) > 0:
#         printFuncao(lista_funcoes_char, "CHAR")

#     if len(lista_funcoes_void) > 0:
#         printFuncao(lista_funcoes_void, "VOID")


# def initEscopo(linha, expressao):
#     global escopo_funcao

#     if "{" in expressao:
#         if not escopo_funcao:
#             escopo_funcao = True
#             return True
#         else:
#             st.logErro(linha, "escopo ja iniciado")
#     return False


# def endEscopo(linha, expressao):
#     global escopo_funcao
#     global dados_escopo_funcao

#     if "}" in expressao:
#         if escopo_funcao:
#             lista_funcoes.append([[definicao, parametros], dados_escopo_funcao])
#             escopo_funcao = False
#             dados_escopo_funcao = []
#             return True
#         else:
#             st.logErro(linha, "} sem escopo")
#     return False


# def getEscopo(linha, expressao):
#     match = re.search(f"{s.reg_funcao.pattern}", expressao)

#     if match:
#         global definicao
#         global parametros

#         if initEscopo(linha, expressao):
#             expressao = expressao.replace("{", "")
#         if endEscopo(linha, expressao):
#             expressao = expressao.replace("}", "")

#         definicao = re.search(f"{s.reg_tipos.pattern}\w+\s*", expressao).group()
#         expressao = expressao.replace(definicao, "")

#         if "(" in expressao:
#             expressao = expressao.replace("(", "")
#         if ")" in expressao:
#             expressao = expressao.replace(")", "")

#         definicao = definicao.strip()
#         definicao = {linha: definicao}

#         parametros = expressao.strip()
#         parametros = {linha: parametros}
#     elif initEscopo(linha, expressao):
#         expressao = expressao.replace("{", "")
#         if endEscopo(linha, expressao):
#             expressao = expressao.replace("}", "")
#     elif endEscopo(linha, expressao):
#         expressao = expressao.replace("}", "")
#     else:
#         if escopo_funcao:
#             dados_escopo_funcao.append({linha: expressao})
#         else:
#             st.logErro(linha, "escopo nao iniciado")
#     return True
