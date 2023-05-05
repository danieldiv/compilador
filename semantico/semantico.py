import sintatico as s
import re

arq = open('files/code.txt','r')
lista = []
for x in arq:
    x = x.strip()
    if(len(x) > 0 and not s.is_valid(x)): lista.append(x)

lista_include = []

for x in lista:
    print(x)

def getInclude(linha):
    if '#include' in linha:
        linha = linha.split()
        
        if(len(linha) > 1): lista_include.append(linha[1])
        else: lista_include.append(linha[0].replace('#include',''))
        return True
    return False

lista_funcoes = []
reg_f = r'(int|float|void){1}\s[\w]+\s?\('

def getFuncoes(linha):
    match = re.search(reg_f,linha)
    if(match):
        sub_string = match.group()
        linha = linha.replace(sub_string,'').replace(')','').replace('{','').strip()
        sub_string = sub_string.replace('(','').strip()
        
        lista_funcoes.append([sub_string, linha])
        return True
    return False

for x in lista:
    if(getInclude(x)): continue
    elif(getFuncoes(x)): continue
    # else: print('Erro na linha: '+x)

for x in lista_funcoes:
    print(x)
   
# lista_int = []
# valor_int = []
# lista_float =[]
# valor_int = []
# nova_lista_int = []
# lista_invalida = []

# for x in lista:
#     if('=' in x):
#         x = x.split('=')
#         aux = x[1].replace(';','')
#         aux = aux.strip()
            
#         x[1].strip()
#         y = x[0]
#         y = y.split()
#         if (y[0] == 'int'):
#             if(y[1] not in nova_lista_int):
#                 lista_int.append([y[1],aux])
#                 nova_lista_int.append(y[1])
#             else:
#                 print('A variavel '+y[1]+' ja tinha sido criada')
#         else:
#             lista_float.append([y[1],aux])
#     else:
#         lista_invalida.append(x)
# reg=re.compile('[\w]+')
# reg1=re.compile('\d.\d')
# reg2=re.compile(r'[+|\-|*|/]')
# reg3=re.compile('\d')

# print("LISTA DE INTS")
# for x in lista_int: 
#     if(re.fullmatch(reg,x[1])):
#        print('A variavel '+x[0]+' esta validada: '+x[1])
#     else:
#         if(re.search(reg2,x[1])):
#             #print(x[1])
#             lista_aux =[]
#             frase = ''
#             for y in x[1]:
#                 if(re.search(reg2,y)):
#                     lista_aux.append(frase)
#                     frase=''
#                 else:
#                     frase = frase + y
#             lista_aux.append(frase)
#             for y in lista_aux:
#                 if(y in nova_lista_int):
#                     print('A variavel '+y+' esta validada')
#                 else:
#                     if(re.fullmatch(reg3,y)):
#                         print('Regra do D: A variavel '+y+' esta validada')
#                     else:
#                         print('A variavel '+y+' nao esta validada')

# print('\nLISTA INVALIDA')        
# for x in lista_invalida:
#     print(x)