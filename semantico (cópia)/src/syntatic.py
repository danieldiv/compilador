import re

reg_comment = re.compile(
    r"((//.*)|(\/\*(.*)\*\/))"
)  # alguns caracteres precisa colocar "\" antes para poder utilizar

reg_include = re.compile(r"#include\s?(<{1}(\w*).h>{1}|\"{1}(\w*).h\"{1})")
reg_tipos = re.compile(r"(int|float|double|char|void)\s+")
reg_cast = re.compile(r"\(\s?(int|float|double|char|void)\s?\)\s?")
reg_operadores = re.compile(r"(\+|\-|\*|\/|\%|\+\+|\-\-)\s?")
reg_comparacao = re.compile(r"(\<|\>|\<=|\>=|==|\!=)\s?")
reg_args = re.compile(r"(int\sargc,\s?char\s\*argv\[\]|void)\s?")

reg_t0 = re.compile(rf"{reg_tipos.pattern}\w+" rf"(\s?,\s?\w+\s?){{,}};")

reg_t1 = re.compile(
    rf"{reg_tipos.pattern}\w+\s?=\s?"
    r"((\w+|\d+\.\d+);|(\w+)\((\w+)"
    rf"(,\s*(\w+)){{,}}\);)"
)


reg_t2 = re.compile(
    rf"({reg_tipos.pattern}){{,1}}\w+\s?=\s?({reg_cast.pattern}){{,1}}\w+\s?"
    rf"({reg_operadores.pattern}({reg_cast.pattern}){{,1}}\w+\s?){{1,}};"
)

reg_funcao = re.compile(
    rf"{reg_tipos.pattern}\w+\s?\(({reg_args.pattern}|({reg_tipos.pattern}\w+)?\s?"
    rf"(,\s?{reg_tipos.pattern}\w+\s?){{,}})\)\s?{{?"
)

reg_printf = re.compile(r'printf\(("(%d|%f)\\n",\s*(\w+)\);|"\w+"\);)')
reg_return = re.compile(r"return\s?(([\w. ]+)\s?;|\(([\w. ]+)[+|\-|*|/]([\w. ]+)\);)")
reg_scanf = re.compile(r'scanf\s?\("(%d|%i|%f|%lf|%s)",\s?&\w+\)\s?;')
reg_chaves = re.compile(r"({|})")

reg_condicional = re.compile(
    rf"(if\s?\(\s?\w+\s?{reg_comparacao.pattern}\w+\s?\)\s?{{)|"
    rf"(else\s?{{)|(else\sif\s?\(\w+\s?{reg_comparacao.pattern}\w+\)\s?{{)"
)

regexs = []

regexs.extend(
    [
        reg_include,
        reg_t0,
        reg_t1,
        reg_t2,
        reg_funcao,
        reg_condicional,
        reg_printf,
        reg_return,
        reg_scanf,
        reg_chaves,
    ]
)

validade = []


def is_valid(key, line):
    new_line = re.sub(r"\s+", " ", line)
    new_line = re.sub(r"\s,", ",", new_line)
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
