#ifndef FILE_HPP__
#define FILE_HPP__

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include "util.hpp"

class File {
private:
    Util u;
public:
    void readFile(std::string path, std::vector<std::string> &vec);
};

void File::readFile(std::string path, std::vector<std::string> &vec) {
    std::ifstream myfile(path);
    std::string line;

    if (myfile.is_open()) {
        while (getline(myfile, line)) {
            u.strip(line);
            if (line.size() > 0) {
                if (u.validarLexico(line))
                    vec.push_back(line);
                else std::cout << "Linha invalida: " << line << std::endl;
            }
        }
        myfile.close();
    } else std::cout << "Nao foi possivel abrir o arquivo" << std::endl;
}

#endif