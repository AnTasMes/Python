#pragma once

#include <iostream>
#include <vector>

namespace CPU {
    struct cpu_instruction {
        int type = -1;
        std::vector<int> arguments;
    };

    struct cpu_function {
        std::string name;
        int instruction_counter = 0;
        std::vector<cpu_instruction> instructions;
        std::vector<std::vector<unsigned char>> data;
        std::vector<int> old_registers;
    };

    std::vector<cpu_function> function_templates;
    std::vector<cpu_function> loaded_functions;
    cpu_function* current_function = nullptr;
    std::vector<int> registers;
    bool halt = false;

    void initCPU() {
        registers.resize(8);
    }

    void load_function(int function_id, const std::vector<std::pair<bool, int>>& arguments) {
        loaded_functions.push_back(function_templates[function_id]); //Dodaje se funkcija na ucitane funkcije
        loaded_functions[loaded_functions.size()-1].data.resize(arguments.size()); //Prosiruju se promenljive na broj argumenata

        int argument_index = 0; //Ucitavaju se argumenti iz registra i iz promenljive prethodne funkcije
        for (auto& i : arguments) {
            if (i.first) {
                loaded_functions[loaded_functions.size()-1].data[argument_index][0] = registers[i.second];
            }else{
                loaded_functions[loaded_functions.size()-1].data[argument_index] = current_function->data[i.second];
            }

            argument_index++;
        }

        if (current_function != nullptr)
            current_function->old_registers = registers; //Cuvaju se trenutne vrednosti registra
        current_function = &loaded_functions[loaded_functions.size()-1];
        current_function->instruction_counter = 0;
    }

    void return_function(std::pair<bool, int> ret) {
        if (loaded_functions.size() > 1) {
            loaded_functions[loaded_functions.size()-2].data.resize(loaded_functions[loaded_functions.size()-2].data.size()+1); //Prosiruju se promenljive za jednu vise u prethodnoj funkciji
            if (ret.first) { //Vraca se vrednost iz registra ili druge promenljive u novu promenljivu u prethodnoj funkciji
                loaded_functions[loaded_functions.size()-2].data[loaded_functions[loaded_functions.size()-2].data.size()-1][0] = registers[ret.second];
            }else{
                loaded_functions[loaded_functions.size()-2].data[loaded_functions[loaded_functions.size()-2].data.size()-1] = current_function->data[ret.second];
            }

            registers = loaded_functions[loaded_functions.size()-2].old_registers; //Vracaju se vrednosti u registre kao pre poziva funkcije
            current_function = &loaded_functions[loaded_functions.size()-2];
            loaded_functions.pop_back(); //Sklanja se vrhovna funkcija iz liste ucitanjih funkcija
        }else{
            halt = true;
        }
    }

    bool tick() {
        if (loaded_functions.size() > 0 and current_function->instruction_counter < current_function->instructions.size() && !halt) {
            current_function = &loaded_functions[loaded_functions.size()-1];
            cpu_instruction* c_ins = &current_function->instructions[current_function->instruction_counter];
            switch(c_ins->type) {
                case 0x0: //U slucaju da je zastava halt tacna, zaustavlja se rad
                    halt = true;
                    break;
                case 0x1: //Ucitavanje drugog argumenta u registar sa indeksom prvog vrednosti argumenta
                    registers[c_ins->arguments[0]] = c_ins->arguments[1];
                    current_function->instruction_counter++;
                    break;
                case 0x2: //Ucitavanje vrednosti iz registra drugog argumenta u registar sa indeksom prvog vrednosti argumenta
                    registers[c_ins->arguments[0]] = registers[c_ins->arguments[1]];
                    current_function->instruction_counter++;
                    break;
                case 0x3: //Ucitavanje vrednosti iz promenljive sa indeksom drugog argumenta i razmakom 0 u registar sa indeksom prvog vrednosti argumenta
                    registers[c_ins->arguments[0]] = current_function->data[c_ins->arguments[1]][0];
                    current_function->instruction_counter++;
                    break;
                case 0x4: //Ucitavanje vrednosti iz promenljive sa indeksom drugog argumenta i razmakom vrednosti treceg argumenta u registar sa indeksom vrednosti prvog argumenta
                    registers[c_ins->arguments[0]] = current_function->data[c_ins->arguments[1]][c_ins->arguments[2]];
                    current_function->instruction_counter++;
                    break;
                case 0x5: //Ucitavanje vrednosti iz promenljive sa indeksom vrednosti iz registra sa indeksom drugog argumenta i razmakom 0 u registar sa indeksom vrednosti prvog argumenta
                    registers[c_ins->arguments[0]] = current_function->data[registers[c_ins->arguments[1]]][0];
                    current_function->instruction_counter++;
                    break;
                case 0x6: //Ucitavanje vrednosti iz promenljive sa indeksom drugog argumenta i razmakom vrednosti iz registra sa indeksom treceg argumenta u registar sa indeksom vrednosti prvog argumenta
                    registers[c_ins->arguments[0]] = current_function->data[c_ins->arguments[1]][registers[c_ins->arguments[2]]];
                    current_function->instruction_counter++;
                    break;
                case 0x7: //Ucitavanje vrednosti iz promenljive sa indeksom vrednosti iz registra sa indeksom drugog argumenta i razmakom vrednosti iz registra sa indeksom vrednosti treceg argumenta u registar sa indeksom vrednosti prvog argumenta
                    registers[c_ins->arguments[0]] = current_function->data[registers[c_ins->arguments[1]]][registers[c_ins->arguments[2]]];
                    current_function->instruction_counter++;
                    break;
                case 0x8: //Cuvanje vrednosti u promenljivu sa indeksom vrednosti prvog argumenta sa razmakom 0 iz registra sa indeksom vrednosti drugog argumenta
                    current_function->data[c_ins->arguments[0]][0] = registers[c_ins->arguments[1]];
                    current_function->instruction_counter++;
                    break;
                case 0x9: //Cuvanje vrednosti u promenjlivu sa indeksom vrednosti prvog argumenta sa razmakom vrednosti drugog argumenta iz registra sa indeksom vrednosti treceg argumenta
                    current_function->data[c_ins->arguments[0]][c_ins->arguments[1]] = registers[c_ins->arguments[2]];
                    current_function->instruction_counter++;
                    break;
                case 0xa: //Cuvanje vrednosti u promenljivu sa indeksom vrednosti registra sa indeksom vrednosti prvog argumenta sa razmakom 0 iz registra sa indeksom vrednosti drugog argumenta
                    current_function->data[registers[c_ins->arguments[0]]][0] = registers[c_ins->arguments[1]];
                    current_function->instruction_counter++;
                    break;
                case 0xb: //Cuvanje vrednosti u promenljivu sa indeksom vrednosti registra sa indeksom vrednosti prvog argumenta sa razmakom vrednosti drugog argumenta iz registra sa indeksom vrednosti treceg argumenta
                    current_function->data[registers[c_ins->arguments[0]]][c_ins->arguments[1]] = registers[c_ins->arguments[2]];
                    current_function->instruction_counter++;
                    break;
                case 0xc: //Cuvanje vrednosti u promenljivu sa indeksom vrednosit registra sa indeksom vrednosti prvog argumenta sa razmakom vrednosti registra sa indeksom vrednosti drugog argumenta iz registra sa indeksom vrednosti treceg argumenta
                    current_function->data[registers[c_ins->arguments[0]]][registers[c_ins->arguments[1]]] = registers[c_ins->arguments[2]];
                    current_function->instruction_counter++;
                    break;
                case 0xd: //Dodavanje vrednosti iz registra sa indeksom vrednosti drugog argumenta u registar sa indeksom vrednosti prvog argumenta
                    registers[c_ins->arguments[0]] += registers[c_ins->arguments[1]];
                    current_function->instruction_counter++;
                    break;
                case 0xe: //Oduzimanje vrednosti iz registra sa indeksom vrednosti prvog argumenta sa vrednoscu iz registra sa indeksom vrednosti drugog argumenta
                    registers[c_ins->arguments[0]] -= registers[c_ins->arguments[1]];
                    current_function->instruction_counter++;
                    break;
                case 0xf: //Mnozenje vrednosti u registru sa indeksom vrednosti prvog argumenta sa vrednoscu iz registra sa indeksom vrednosti drugog argumenta
                    registers[c_ins->arguments[0]] *= registers[c_ins->arguments[1]];
                    current_function->instruction_counter++;
                    break;
                case 0x10: //Deljenje vrednosti iz registra sa indeksom vrednosti prvog argumenta sa vrednoscu iz registra sa indeksom vrednosti drugog argumenta
                    //U slucaju da je u drugom registru vrednost 0, stampa se greska i zaustavlja se virtuelna masina
                    if (registers[c_ins->arguments[1]] == 0) {
                        std::cerr << "ERROR, CANNOT DIVIDE WITH ZERO. STOPPING.\n";
                        halt = true;
                    }else{
                        registers[c_ins->arguments[0]] /= registers[c_ins->arguments[1]];
                    }
                    current_function->instruction_counter++;
                    break;
                case 0x11: //Provera da li je vrednosti u registru sa indeksom vrednosti drugog argumenta veca od vrednosti u registru sa indeksom vrednosti drugog argumenta i cuvanje rezultata u registar sa indeksom vrednosti prvog argumenta
                    registers[c_ins->arguments[0]] = registers[c_ins->arguments[1]] > registers[c_ins->arguments[2]];
                    current_function->instruction_counter++;
                    break;
                case 0x12: //Provera da li je vrednosti u registru sa indeksom vrednosti drugog argumenta veca ili jednaka od vrednosti u registru sa indeksom vrednosti drugog argumenta i cuvanje rezultata u registar sa indeksom vrednosti prvog argumenta
                    registers[c_ins->arguments[0]] = registers[c_ins->arguments[1]] >= registers[c_ins->arguments[2]];
                    current_function->instruction_counter++;
                    break;
                case 0x13: //Provera da li je vrednosti u registru sa indeksom vrednosti drugog argumenta manja od vrednosti u registru sa indeksom vrednosti drugog argumenta i cuvanje rezultata u registar sa indeksom vrednosti prvog argumenta
                    registers[c_ins->arguments[0]] = registers[c_ins->arguments[1]] < registers[c_ins->arguments[2]];
                    current_function->instruction_counter++;
                    break;
                case 0x14: //Provera da li je vrednosti u registru sa indeksom vrednosti drugog argumenta manja ili jednaka od vrednosti u registru sa indeksom vrednosti drugog argumenta i cuvanje rezultata u registar sa indeksom vrednosti prvog argumenta
                    registers[c_ins->arguments[0]] = registers[c_ins->arguments[1]] <= registers[c_ins->arguments[2]];
                    current_function->instruction_counter++;
                    break;
                case 0x15: //Provera da li je vrednosti u registru sa indeksom vrednosti drugog argumenta jednaka sa vrednosti u registru sa indeksom vrednosti drugog argumenta i cuvanje rezultata u registar sa indeksom vrednosti prvog argumenta
                    registers[c_ins->arguments[0]] = registers[c_ins->arguments[1]] == registers[c_ins->arguments[2]];
                    current_function->instruction_counter++;
                    break;
                case 0x16: //Provera da li je vrednosti u registru sa indeksom vrednosti drugog argumenta razlicita od vrednosti u registru sa indeksom vrednosti drugog argumenta i cuvanje rezultata u registar sa indeksom vrednosti prvog argumenta
                    registers[c_ins->arguments[0]] = registers[c_ins->arguments[1]] != registers[c_ins->arguments[2]];
                    current_function->instruction_counter++;
                    break;
                case 0x17: //Promena brojaca instrukcije u vrednost prvog argumenta
                    current_function->instruction_counter = c_ins->arguments[0];
                    break;
                case 0x18: //Promena brojaca instrukcije u vrednost u registru sa indeksom vrednosti prvog argumenta
                    current_function->instruction_counter = registers[c_ins->arguments[0]];
                    break;
                case 0x19:
                    if (registers[c_ins->arguments[0]] == 0) { //Proverava se da li vrednost u registru sa indeksom vrednosti prvog argumenta 0
                        current_function->instruction_counter = c_ins->arguments[1]; //U slucaju da jeste, menja se brojac instrukcije u vrednost drugog argumenta
                    }else{
                        current_function->instruction_counter++; //U slucaju da nije, povecava se brojac instrukcije
                    }
                    break;
                case 0x1a:
                    if (registers[c_ins->arguments[0]] == 0) { //Proverava se da li vrednost u registru sa indeksom vrednosti prvog argumenta 0
                        current_function->instruction_counter = registers[c_ins->arguments[1]]; //U slucaju da jeste, menja se brojac instrukcije u vrednost u registru sa indeksom vrednosti drugog argumenta
                    }else{
                        current_function->instruction_counter++; //U slucaju da nije, povecava se brojac instrukcije
                    }
                    break;
                case 0x1b:
                    if (registers[c_ins->arguments[0]] == 1) { //Proverava se da li vrednost u registru sa indeksom vrednosti prvog argumenta 1
                        current_function->instruction_counter = c_ins->arguments[1]; //U slucaju da jeste, menja se brojac instrukcije u vrednost drugog argumenta
                    }else{
                        current_function->instruction_counter++; //U slucaju da nije, povecava se brojac instrukcije
                    }
                    break;
                case 0x1c:
                    if (registers[c_ins->arguments[0]] == 1) { //Proverava se da li vrednost u registru sa indeksom vrednosti prvog argumenta 1
                        current_function->instruction_counter = registers[c_ins->arguments[1]]; //U slucaju da jeste, menja se brojac instrukcije u vrednost u registru sa indeksom vrednosti drugog argumenta
                    }else{
                        current_function->instruction_counter++; //U slucaju da nije, povecava se brojac instrukcije
                    }
                    break;
                case 0x1d: //Stampa se vrednost u registru sa indeksom vrednosti prvog argumenta
                    std::cout << registers[c_ins->arguments[0]];
                    current_function->instruction_counter++;
                    break;
                case 0x1e: //Stampa se vrednost u registru sa indeksom vrednosti prvog argumenta i stampa se novi red
                    std::cout << registers[c_ins->arguments[0]] << '\n';
                    current_function->instruction_counter++;
                    break;
                case 0x1f: //Stampa se vrednost u obliku karaktera u registru sa indeksom vrednosti prvog argumenta
                    std::cout << (char)registers[c_ins->arguments[0]];
                    current_function->instruction_counter++;
                    break;
                case 0x20: //Stampa se vrednost u obliku karaktera u registru sa indeksom vrednosti prvog argumenta i sampa se novi red
                    std::cout << (char)registers[c_ins->arguments[0]] << '\n';
                    current_function->instruction_counter++;
                    break;
                case 0x21: //Stampaju se svi elementi u promenljivoj sa indeksom vrednosti prvog argumenta
                    for (auto& i : current_function->data[c_ins->arguments[0]]) {
                        std::cout << i;
                    }
                    current_function->instruction_counter++;
                    break;
                case 0x22: //Stampaju se svi elementi u promenljivoj sa indeksom vrednosti prvog argumenta i stampa se razmak posle svakog elementa
                    for (auto& i : current_function->data[c_ins->arguments[0]]) {
                        std::cout << i << ' ';
                    }
                    current_function->instruction_counter++;
                    break;
                case 0x23: //Stampaju se svi elementi u promenljivoj u obliku karaktera sa indeksom vrednosti prvog argumenta
                    for (auto& i : current_function->data[c_ins->arguments[0]]) {
                        std::cout << (char)i;
                    }
                    current_function->instruction_counter++;
                    break;
                case 0x24: //Stampaju se svi elementi u promenljivoj u obliku karaktera sa indeksom vrednosti provg argumenta i sampa se razmak posle svakog elementa
                    for (auto& i : current_function->data[c_ins->arguments[0]]) {
                        std::cout << (char)i << ' ';
                    }
                    current_function->instruction_counter++;
                    break;
                case 0x25: //Menja se broj promenljivih u vrednost prvog argumenta
                    current_function->data.resize(c_ins->arguments[0]);
                    current_function->instruction_counter++;
                    break;
                case 0x26: //Menja se broj promenljivih u vrednost iz registra sa indeksom vrednosti prvog argumenta
                    current_function->data.resize(registers[c_ins->arguments[0]]);
                    current_function->instruction_counter++;
                    break;
                case 0x27: //Menja se broj elemenata u promenljivoj sa indeskom prvog argumenta u vrednost drugog argumenta
                    current_function->data[c_ins->arguments[0]].resize(c_ins->arguments[1]);
                    current_function->instruction_counter++;
                    break;
                case 0x28: //Menja se broj elemenata u promenljivoj sa indeksom vrednosti iz registra sa indeksom vrednosti provg argumenta u vrednost drugog argumenta
                    current_function->data[registers[c_ins->arguments[0]]].resize(c_ins->arguments[1]);
                    current_function->instruction_counter++;
                    break;
                case 0x29: //Menja se broj elemenata u promenjlivoj sa indeksom vrednosti prvog argumenta u vrednost iz registra sa indeksom vrednosti drugog argumenta
                    current_function->data[c_ins->arguments[0]].resize(registers[c_ins->arguments[1]]);
                    current_function->instruction_counter++;
                    break;
                case 0x2a: //Menja se broj elemenata u promenjlivoj sa indeksom vrednosti iz registra sa indeksom vrednosti prvog argumenta u vrednost iz registra sa indeksom vrednosti drugog argumenta
                    current_function->data[registers[c_ins->arguments[0]]].resize(registers[c_ins->arguments[1]]);
                    current_function->instruction_counter++;
                    break;
                case 0x2b: { //Poziva se funkcija
                    std::vector<std::pair<bool, int>> arguments;

                    for (int i = 1; i < c_ins->arguments.size(); i += 2) { //Ide u parovima, prvi je da li je argument u registru, drugi element je indeks
                        arguments.emplace_back(std::make_pair((bool)c_ins->arguments[i], c_ins->arguments[i+1]));
                    }

                    load_function(c_ins->arguments[0], arguments); //prvi argument je id funkcije
                }
                    break;
                case 0x2c: { //Vraca se funkcija
                    return_function(std::make_pair((bool)c_ins->arguments[0], c_ins->arguments[1])); //prvi argument je da li se vrednost vraca u registar i drugi argument je indeks
                }
                    break;
                case 0x2d: { //Ucitavanje stringa, prvi argument je indeks promenljive koja ce sadrzati string
                    std::string input;
                    std::cin >> input;

                    current_function->data[c_ins->arguments[0]].resize(input.length());

                    for (auto& i : input) {
                        current_function->data[c_ins->arguments[0]].push_back(static_cast<int>(i));
                    }

                    current_function->instruction_counter++;
                }
                    break;
                case 0x2e: { //Pretvaranje vrednosti iz registra u zasebne znakove, prvi argument je iz kog registra se uzima vrednost a drugi argument je indeks promenljive gde ce biti sacuvano
                    std::string input = std::to_string(registers[c_ins->arguments[0]]);

                    current_function->data[c_ins->arguments[1]].resize(input.length());

                    for (auto& i : input) {
                        current_function->data[c_ins->arguments[1]].push_back(static_cast<int>(i));
                    }

                    current_function->instruction_counter++;
                }
                    break;
                case 0x2f:
                    std::cout << registers[0] << ' ' << registers[1] << ' ' << registers[2] << ' ' << registers[3] << ' ' << registers[4] << ' ' << registers[5] << ' ' << registers[6] << ' ' << registers[7] << '\n';
                    current_function->instruction_counter++;
                    break;
                default:
                    std::cerr << "Unknown instruction: " << c_ins->type << ", stopping.\n";
                    halt = true;
                    break;
            }
            return true;
        }else{
            return false;
        }
    }
}