#include <iostream>
#include <regex>

using std::cout;
using std::endl;

void printMatches(std::string str, std::regex reg) {
    std::smatch matches;
    cout << std::boolalpha;

    while (std::regex_search(str, matches, reg)) {
        // cout << "Is there a match : " << matches.ready() << endl;
        // cout << "Are there no matches : " << matches.empty() << endl;
        // cout << "number of matches : " << matches.size() << endl;
        cout << matches.str(1) << endl;
        str = matches.suffix().str();
        cout << endl;
    }
}

void printMatches2(std::string str, std::regex reg) {
    std::sregex_iterator currentMatch(str.begin(), str.end(), reg);
    std::sregex_iterator lastMatch;

    while (currentMatch != lastMatch) {
        std::smatch match = *currentMatch;
        cout << match.str() << endl;
        currentMatch++;
    }
    cout << endl;
}

int main() {
    // qualquer coisa que nao seja espaco
    std::string str = "The ape was at the apex";
    std::regex reg("(ape[^ ]?)");
    printMatches(str, reg);

    // pega as palavras que possuem pick e o restante da palavra
    std::string str2 = "I picked the pickle";
    std::regex reg2("(pick([^ ]+)?)");
    printMatches2(str2, reg2);

    // pega as palavras que iniciam com crmfp, menos o Cat, C eh maiusculo
    std::string str3 = "Cat rat mat fat pat";
    std::regex reg3("([crmfp]at)");
    printMatches2(str3, reg3);

    // Cat fat
    std::regex reg4("([C-Fc-f]at)");
    printMatches2(str3, reg4);

    // pode comecar com C ou r
    std::regex reg5("([Cr]at)");
    printMatches2(str3, reg5);

    // nao pode comecar com C ou r
    std::regex reg6("([^Cr]at)");
    printMatches2(str3, reg6);

    // substitui as palavaras que comecam com C ou r por Owl
    std::string owlFood = std::regex_replace(str3, reg5, "Owl");
    cout << owlFood << endl;

    // 1 ponto mais alguma coisa, 1 ponto mais alguma coisa, 1 pont
    std::string str7 = "F.B.I. F.BB.I. I.R.S. CIA";
    std::regex reg7("([^ ]\\..\\..\\.)");
    printMatches2(str7, reg7);

    // substitui \n por espaco
    std::string str8 = "This is a\nmultiline string\n"
        "that has many lines";
    std::regex reg8("\n");
    std::string noLBStr = std::regex_replace(str8, reg8, " ");
    cout << noLBStr << endl;

    // \d [0-9] pega apenas numeros
    // \D [^0-9] nao pega numeros
    std::string str9 = "12345";
    std::regex reg9("\\d");
    printMatches2(str9, reg9);

    // pega entre 5 a 7 caracteres, os que possuem menos nao pega, quando passa pega o maximo
    std::string str10 = "123 12345 123456 1234567 12346111118";
    std::regex reg10("\\d{5,7}");
    printMatches2(str10, reg10);

    // \w [a-zA-Z0-9] pega numeros e letras
    // \W [^a-zA-Z0-9] nao pega numeros nem letras
    // 3 numeros seta 3 numeros seta 3 numeros seta -> so pega se atender o padrao
    std::string str11 = "412-867-5309";
    std::regex reg11("\\w{3}-\\w{3}-\\w{4}");
    printMatches2(str11, reg11);

    // \s [\f\n\r\t\v]
    // \S [^\f\n\r\t\v]

    // \f -> quebra a linha e coloca espacos para alinhar com a frase de cima
    // \n -> quebra de linha
    // \r -> nao entendi pra que serve
    // \t -> tabulacao
    // \v -> obteve o mesmo que \f

    // verifica se o nome eh valido
    std::string str12 = "Toshio Muramatsu";
    std::regex reg12("\\w{2,20}\\s\\w{2,20}");
    printMatches2(str12, reg12);

    // deve iniciar com a e ter apenas letras seguidas
    std::string str13 = "a as ape bug armamento";
    std::regex reg13("a[a-z]+");
    printMatches2(str13, reg13);

    // ----- PROBLEM -----
    // Create a Regex that matches email addresses 
    // from a list
    // 1. 1 to 20 lowercase and uppercase letters, numbers, plus ._%+-
    // 2. An @ symbol
    // 3. 2 to 20 lowercase and uppercase letters, numbers, plus .-
    // 4. A period
    // 5. 2 to 3 lowercase and uppercase letters

    std::string str14 = "db@aol.com m@.com @apple.com db@.com";
    std::regex reg14("[\\w._%+-]{1,20}@[\\w.-]{2,20}.[A-Za-z]{2,3}");
    printMatches2(str14, reg14);

    return 0;
}