#include <iostream>

#include "CPU.h"

int main() {

    CPU::initCPU();

    CPU::cpu_function test;

    test.instructions.push_back({1, {0, 5}});
    test.instructions.push_back({1, {1, 10}});
    test.instructions.push_back({0xd, {0, 1}});
    test.instructions.push_back({0x1e, {0}});
    test.instructions.push_back({0x2f, {}});

    CPU::function_templates.push_back(test);

    CPU::load_function(0, {});

    while (CPU::tick()) {

    }

    return 0;
}
