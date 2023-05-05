import sintatico as s
import re

arq = open('files/code.txt','r')
lista = []
for x in arq:
    x = x.strip()
    if(len(x) > 0 and s.is_valid(x)): lista.append(x)

lista_include = []

# for x in lista:
#     print(x)

def getInclude(linha):
    if '#include' in linha:
        linha = linha.split()
        
        if(len(linha) > 1): lista_include.append(linha[1])
        else: lista_include.append(linha[0].replace('#include',''))
        return True
    return False

lista_funcoes = []
lista_escopo = []
reg_f1 = f'{s.reg_tipos.pattern}\w+\s*'

escopo_atual = False
sub_string = ''
parametros = ''

def getFuncoes(linha):
    match = re.search(reg_f1,linha)
    
    global sub_string
    global escopo_atual
    global parametros
    global lista_escopo
    
    if(match and '=' not in linha):
        sub_string = match.group()
        linha = linha.replace(sub_string,'')
        
        if('{' in linha):
            escopo_atual = True
            linha = linha.replace('{','')
        
        if('(' in linha): linha = linha.replace('(','')
        if(')' in linha): linha = linha.replace(')','')
        
        sub_string = sub_string.strip()
        parametros = linha.strip()
        
        return True
    elif('{' in linha):
        escopo_atual = True
        return True
    elif('}' in linha):
        lista_funcoes.append([[sub_string, parametros], lista_escopo])
        escopo_atual = False
        lista_escopo = []
        return True
    elif(escopo_atual):
        lista_escopo.append(linha)
        return True
    return False

for x in lista:
    if(getInclude(x)): continue
    elif(getFuncoes(x)): continue
    else: print('Erro na linha: '+x)

for x in lista_funcoes:
    print(x[0])
    for y in x[1]:
        print(y)
    print()
    
   
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