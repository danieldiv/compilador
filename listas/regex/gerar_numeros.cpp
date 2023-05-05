#include <iostream>
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <regex>

using namespace std;

string checkMatches(std::string str, std::regex reg) {
    std::sregex_iterator currentMatch(str.begin(), str.end(), reg);
    std::sregex_iterator lastMatch;
    string res = "";

    while (currentMatch != lastMatch) {
        std::smatch match = *currentMatch;
        res.assign(match.str());
        currentMatch++;
    }
    return res;
}

pair<int, int> getIntervalo(std::string str, std::regex reg) {
    std::sregex_iterator currentMatch(str.begin(), str.end(), reg);
    std::sregex_iterator lastMatch;

    bool aux = true;
    int val = 0;

    while (currentMatch != lastMatch) {
        std::smatch match = *currentMatch;

        if (aux) val = stoi(match.str());
        else return make_pair(val, stoi(match.str()));

        aux = (aux) ? false : aux;
        currentMatch++;
    }
    return make_pair(0, 1);
}

#define get_number(aux_, reg_, res_) (aux_.size() != 0) ? stoi(checkMatches(aux_, reg_)) : res_

int main(int argc, char **argv) {
    string str("");

    for (int i = 1; i < argc; i++) str.append(argv[i]).append(" ");

    std::regex reg_inteiro("-i");
    std::regex reg_quant("-n \\d{1,2}");
    std::regex reg_intervalo("-r \\d{1,7} \\d{1,7}");
    std::regex reg_decimal("-p \\d{1}");
    std::regex reg_seed("-s \\d{1,4}");
    std::regex reg_number("\\d{1,2}");
    std::regex reg_LI_LS("\\d{1,7}");

    bool inteiro = checkMatches(str, reg_inteiro).size() != 0;
    int x = get_number(checkMatches(str, reg_quant), reg_number, 1);
    int X = get_number(checkMatches(str, reg_decimal), reg_number, 4);
    int seed = get_number(checkMatches(str, reg_seed), reg_number, -1);

    double val;

    pair<int, int>intervalo = getIntervalo(checkMatches(str, reg_intervalo), reg_LI_LS);

    int LI = intervalo.first;
    int LS = intervalo.second;

    if (seed >= 0) srand(seed);
    else srand(time(NULL));

    for (int i = 0; i < x; i++) {
        val = (inteiro) ? (LI + rand() % (LS - LI)) : ((LI + (double)rand() * (LS - LI)) / (double)RAND_MAX);
        cout << fixed << setprecision(X) << val << " ";
    }
    cout << endl;

    return 0;
}