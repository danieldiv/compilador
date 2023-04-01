
// #include <algorithm>
// #include <iostream>
// #include <fstream>
// #include <chrono>

// #include "const.hpp"

// using namespace std;
// using namespace std::chrono;

// int main() {
//     vector<string> words;
//     words.push_back("aah");
//     words.push_back("aal");
//     words.push_back("int");

//     cout << binary_search(words.begin(), words.end(), "float") << endl;

//     return 0;
// }


#include <algorithm>
#include <iostream>
#include <fstream>
#include <chrono>

#include "const.hpp"

using namespace std;
using namespace std::chrono;

bool validar_lexico(string linha) {
    for (auto l : linha) {
        if ((int)l < 0 || (int)l > 127) { // ((int)l < 32 || (int)l > 126)
            return false;
        }
    }
    return true;
}

bool readFile(string path, vector<string> &vec) {
    ifstream myfile(path);
    string line;

    if (myfile.is_open()) {
        while (getline(myfile, line)) {
            if (!validar_lexico(line)) return false;
            vec.push_back(line);
        }
        myfile.close();
    } else cout << "Nao foi possivel abrir o arquivo" << endl;
    return true;
}

void get_tokens(vector<string> vec) {
    for (auto rw : RESERVERD_WORDS) {
        cout << rw << endl;
    }
    cout << endl;
    cout << binary_search(RESERVERD_WORDS.begin(), RESERVERD_WORDS.end(), "float") << endl;
}

int main() {
    vector<string> v_linhas;
    steady_clock::time_point t1 = steady_clock::now();

    if (readFile("file.txt", v_linhas)) {

        for (auto v : v_linhas) {
            cout << v << endl;
        }
        get_tokens(v_linhas);
    } else {
        cout << "Os caracteres informados sao invalidos" << endl;
    }

    steady_clock::time_point t2 = steady_clock::now();
    double tempo = duration_cast<duration<double>>(t2 - t1).count();

    cout << "tempo total: " << tempo << endl;

    return 0;
}