import re

reg_comment = re.compile(
    r"((//.*)|(\/\*(.*)\*\/))"
)  # alguns caracteres precisa colocar "\" antes para poder utilizar

reg_include = re.compile(r"#include\s?(<{1}(\w*).h>{1}|\"{1}(\w*).h\"{1})")
reg_tipos = re.compile(r"(int|float|double|char|void)\s+")

reg_t0 = re.compile(rf"{reg_tipos.pattern}\w+" rf"(\s?,\s?\w+\s?){{,}};")

reg_t1 = re.compile(
    rf"{reg_tipos.pattern}\w+\s?=\s?"
    r"([\d]+;|(\w+);|(\w+)\((\w+)"
    rf"(,\s*(\w+)){{,}}\);)"
)

reg_funcao = re.compile(
    rf"{reg_tipos.pattern}\w+\s?\((void|({reg_tipos.pattern}\w+)?\s?"
    rf"(,\s?{reg_tipos.pattern}\w+\s?){{,}})\)\s?{{?"
)

reg_printf = re.compile(r'printf\(("(%d|%f)\\n",\s*(\w+)\);|"\w+"\);)')
reg_return = re.compile(r"return\s?(([\w. ]+)\s?;|\(([\w. ]+)[+|\-|*|/]([\w. ]+)\);)")
reg_scanf = re.compile(r'scanf\s?\("(%d|%i|%f|%lf|%s)",\s?&\w+\)\s?;')
reg_chaves = re.compile(r"({|})")

regexs = []

regexs.extend(
    [
        reg_include,
        reg_t0,
        reg_t1,
        reg_funcao,
        reg_printf,
        reg_return,
        reg_scanf,
        reg_chaves,
    ]
)

validade = []


def is_valid(key, line):
    new_line = re.sub(r"\s+", " ", line)
    line = new_line

    for reg in regexs:
        match = re.fullmatch(reg, line)
        if match:
            validade.append({key: match.group()})
            return True
        elif "//" in line or "/*" in line:
            reg_aux = re.compile(f"{reg.pattern}\s?{reg_comment.pattern}")
            match = re.fullmatch(reg_aux, line)
            if match:
                match_split = re.match(reg, line)
                validade.append({key: match_split.group()})
                return True
    return False
