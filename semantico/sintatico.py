import re

reg_include = re.compile(r'#include\s?<{1}(\w*).h>{1}')
reg_tipos = re.compile(r'(int|float|double|char|void)\s+')

reg_t1 = re.compile(f'{reg_tipos.pattern}\w\s?=\s?'
                    r'([\d]+;|(\w+)\((\w+),(\w+)\);)')

reg_t2 = re.compile(f'{reg_tipos.pattern}\w+\s?\('
                    f'{reg_tipos.pattern}\w+\s?,\s?'
                    f'{reg_tipos.pattern}\w+\)\s?{{')

reg_printf = re.compile(r'printf\(("%d\\n",\s(\w+)\);|"\w+"\);)')
reg_return = re.compile(r'return\s+((\w+)\s?;|\((\w+)[+|\-|*|/](\w+)\);)')
reg_main = re.compile(r'int (main)\s?\((void)?\)\s?{')
reg_scanf = re.compile(r'scanf\s?\("%d",\s?&\w+\)\s?;')
reg_chaves = re.compile(r'({|})')

regexs = []

regexs.append(reg_include)
regexs.append(reg_t1)
regexs.append(reg_t2)
regexs.append(reg_printf)
regexs.append(reg_return)
regexs.append(reg_main)
regexs.append(reg_scanf)
regexs.append(reg_chaves)

def is_valid(line):
    for reg in regexs:
        match = re.search(reg, line)
        if(match):
            return True
    return False