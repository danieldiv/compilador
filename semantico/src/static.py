INT = "int"
FLOAT = "float"
DOUBLE = "double"
CHAR = "char"
VOID = "void"

RED = "\033[1;31m"
BLUE = "\033[0;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
GRAY = "\033[0;30m"
YELLOW = "\033[0;33m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"


def isFloat(string):
    try:
        float(string)
        return True
    except:
        return False


def logErro(linha, msg):
    print(f"{RED}Erro:{RESET} linha {linha} {msg}")
    exit()


def logWarning(linha, msg):
    print(f"{YELLOW}Warning: {GRAY}linha {linha} {msg}{RESET}")
