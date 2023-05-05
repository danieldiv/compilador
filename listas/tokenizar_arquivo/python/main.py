arquivo = open("file.txt","r")
reserved = open("reserved.txt","r")

lista = []
res = []

for r in reserved: lista.append(r.strip())

def check_frase(frase):
    frase = frase.strip()
    if(len(frase) != 0): res.append(frase)

for x in arquivo:
    x = x.strip()
    frase = ""
    
    for y in x:
        if(y not in lista or y == " "):
            frase = frase + y
            
            if(frase in lista):
                check_frase(frase)
                frase = ""
        else:
            check_frase(frase)
            check_frase(y)
            frase = ""
    check_frase(frase)
            
for i in res: print(i)