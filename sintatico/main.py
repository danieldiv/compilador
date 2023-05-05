import re

code = open("files/code.txt", "r")
lista = []

for line in code:
    line = line.strip()
    if(len(line) > 0): lista.append(line)

reg1 = re.compile(r'#include\s?<{1}(\w*).h>{1}')
reg2 = re.compile(r'(int|float)\s+[A-Za-z]\s?=\s?([\d]+;|([a-z]+)\(([a-z]+|\d+),([a-z]+|\d+)\);)')
reg3 = re.compile(r'printf\("%d\\n",\s([a-z]+|\d+)\);')
reg4 = re.compile(r'return\s+([a-z]+|\d+)\s?;')
reg5 = re.compile(r'return\s+\(([a-z]+|\d+)[+|\-|*|/]([a-z]+|\d+)\);')
reg6 = re.compile(r'(int|float){1}\s[a-z]+\s?\((int|float)\s+[a-z]+\s?,\s?(int|float)\s+[a-z]+\)\s?{')
reg7 = re.compile(r'int main\s?\(void\)\s?{')
reg8 = re.compile(r'scanf\s?\("%d",\s?&[a-z]+\)\s?;')
reg9 = re.compile(r'({|})')

regexs = []

regexs.append(reg1)
regexs.append(reg2)
regexs.append(reg3)
regexs.append(reg4)
regexs.append(reg5)
regexs.append(reg6)
regexs.append(reg7)
regexs.append(reg8)
regexs.append(reg9)

valido = []
invalido = []

for l in lista:
    match = re.search(reg1, l)
    
    aux = True
    for reg in regexs:
        match = re.search(reg, l)
        if(match):
            valido.append(match.group())
            aux = False
            break
    if(aux): invalido.append(l)
        
print("valido\n")
for v in valido: print(v)

print("\ninvalido\n")
for i in invalido: print(i)