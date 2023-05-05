import re

def q1_a(reg):
    print("\nQuestao 1-a\n")
    print(reg.match("das.29@outlook.comcom"))
    print(reg.fullmatch("das.29@outlook.comcom"))
    print(reg.match("das.29@outlook.com.com"))
    print(reg.match("das.29@outlook.comqualquercoisas"))
    print(reg.fullmatch("das.29@outlook.comqualquercoisas"))
    print(reg.fullmatch("das.29@outlook.com.com"))
    print(reg.match("das.29@outlook.com"))
    print(reg.match("das.29@outlook.br"))
    print(reg.match("das.29@outlook.net"))
    print(reg.match("das.29@out&look.br"))
    print(reg.match("das.29@outlook."))
    print(reg.match("das29@outlookcom"))

def q1_b(reg):
    print("\nQuestao 1-b\n")
    print(reg.match("(23) 22022 - 9877"))
    print(reg.match("(23) 22022-9877"))
    print(reg.match("(87) 23456 - 9808"))
    print(reg.match("(23) 22022 - 98779"))
    print(reg.fullmatch("(23) 22022 - 98779"))
    
def q1_c(reg):
    print("\nQuestao 1-c\n")
    print(reg.fullmatch("123.456.789-12"))
    print(reg.fullmatch("111.444.711-62"))
    print(reg.fullmatch("111.444.71-62"))
    
reg1 = re.compile('([\w._]*)@([\w]*).[com|br]{1}')
q1_a(reg1)

reg2 = re.compile(r'\(\d\d\)\s[\d]{5}\s-\s[\d]{4}')
q1_b(reg2)

reg3 = re.compile(r'[\d]{3}.[\d]{3}.[\d]{3}-[\d]{2}')
q1_c(reg3)

print("\nQuestao 2\n")

reg4 = re.compile(r'#include\s?<[a-z.]+>')
reg5 = re.compile(r'return \d;')
reg6 = re.compile(r'(int|float)\s?=\s?(\d*);')

print(reg4.fullmatch("#include <stdio.h>"))
print(reg4.fullmatch("#include <std9io.h>"))
print(reg4.fullmatch("#include<stdio.h>"))
print(reg6.fullmatch("int = 5;"))
print(reg6.fullmatch("int =4;"))
print(reg6.fullmatch("float =5;"))
print(reg6.fullmatch("float = 455;"))
print(reg5.fullmatch("return 0"))
print(reg5.fullmatch("return 0;"))
print(reg5.fullmatch("return 1;"))
print(reg5.fullmatch("return a;"))