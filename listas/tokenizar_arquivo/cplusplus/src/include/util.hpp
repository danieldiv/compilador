#ifndef UTIL_HPP__
#define UTIL_HPP__

#include <string>
#include <regex>

class Util {
private:
    std::regex reg_;
public:
    Util():reg_(R"([\w\s"'!@#$%&*(){}\[\]\|\<\>\,\.\:\;\?\/*\-\+\=\\]*)") { }
    void strip(std::string &str);
    bool validarLexico(std::string str);
};

void Util::strip(std::string &str) {
    if (str.length() == 0) return;

    auto start_it = str.begin();
    auto end_it = str.rbegin();
    while (std::isspace(*start_it)) {
        ++start_it;
        if (start_it == str.end()) break;
    }
    while (std::isspace(*end_it)) {
        ++end_it;
        if (end_it == str.rend()) break;
    }
    int start_pos = start_it - str.begin();
    int end_pos = end_it.base() - str.begin();
    str = start_pos <= end_pos ? std::string(start_it, end_it.base()) : "";
}

bool Util::validarLexico(std::string str) {
    std::sregex_iterator currentMatch(str.begin(), str.end(), reg_);
    std::sregex_iterator lastMatch;

    return currentMatch != lastMatch;
}

#endif