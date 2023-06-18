INT = "int"
FLOAT = "float"
DOUBLE = "double"
CHAR = "char"
VOID = "void"


def isFloat(string):
    try:
        float(string)
        return True
    except:
        return False


def logErro(linha, msg):
    print(f"Erro: linha {linha} {msg}")
    exit()
