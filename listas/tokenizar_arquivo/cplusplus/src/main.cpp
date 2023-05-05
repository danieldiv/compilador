#include <iostream>
#include <string>
#include <algorithm>

#include "include/file.hpp"

using std::cout;
using std::endl;

void print_values(std::string v) { cout << v << endl; }

int main() {
    File f;

    std::vector<std::string> lines;
    std::vector<std::string> reserved;
    std::vector<std::string> tokens;

    f.readFile("files/file.txt", lines);
    f.readFile("files/reserved.txt", reserved);

    // std::for_each(lines.begin(), lines.end(), print_values);
    // std::for_each(reserved.begin(), reserved.end(), print_values);

    std::string aux("");

    std::sort(reserved.begin(), reserved.end());

    for (auto words : lines) {
        for (auto w : words) {
            aux.push_back(w);

            if (std::binary_search(reserved.begin(), reserved.end(), aux)) {
                tokens.push_back(aux);
                cout << "[" << aux << "]" << endl;
                aux.clear();
            } else
                cout << aux << endl;
        }
    }
    // std::for_each(tokens.begin(), tokens.end(), print_values);

    return EXIT_SUCCESS;
}