#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

/* 
   MOJO JOJO'S LAZY LAB
   "I Mojo Jojo shall defeat the Powerpuff Girls with my Lazy Linker!"
*/

// Global buffers
char chemical_x[100];
long dna_sequences[10];

void lab_win() {
    const char *msg = "\n[MOJO JOJO]: NOOOOO! You have compromised my laboratory!\n";
    write(1, msg, strlen(msg));
    system("/bin/sh");
    exit(0);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void print_str(const char *s) {
    write(1, s, strlen(s));
}

void banner() {
    print_str("        _---_        \n");
    print_str("       /     \\      \n");
    print_str("      | () () |     \n");
    print_str("       \\  ^  /      \n");
    print_str("        |||||       \n");
    print_str("      /-------\\     \n");
    print_str("     | MOJO JO |    \n");
    print_str("     |   LAB   |    \n");
    print_str("      \\_______/     \n");
    print_str("\n[MOJO JOJO]: Welcome to my secret laboratory!\n");
    print_str("I, Mojo Jojo, am the most brilliant monkey in the world!\n\n");
}

int get_input() {
    char buf[16];
    if (fgets(buf, sizeof(buf), stdin) == NULL) exit(0);
    return atoi(buf);
}

int main() {
    setup();
    banner();
    
    print_str("[LAB-SCANNER]: Input your Chemical X formula: ");
    if (fgets(chemical_x, sizeof(chemical_x), stdin) == NULL) exit(0);
    
    if (strchr(chemical_x, '%')) {
        print_str("[MOJO JOJO]: CURSES! Powerpuff Girls trickery detected!\n");
        exit(1);
    }

    while(1) {
        print_str("\n--- Laboratory Terminal ---\n");
        print_str("1. Modify DNA Sequence\n");
        print_str("2. Synthesize Chemical X\n");
        print_str("3. Abandon Laboratory\n");
        print_str("> ");
        
        int choice = get_input();
        
        if (choice == 1) { // DNA Modification (OOB Write)
            print_str("DNA Slot Index: ");
            int idx = get_input();
            print_str("Base Pair Value: ");
            int val = get_input();
            
            unsigned short *modifier = (unsigned short*)dna_sequences;
            // The Monkey Math: XOR the index to hide the target
            modifier[idx ^ 0x7050] = (unsigned short)val;
            
            print_str("[LAB]: DNA sequence updated successfully.\n");
        } 
        else if (choice == 2) { // Synthesis (Echo/Printf)
            print_str("[SYNTHESIZER]: Processing formula: ");
            // This is where the GOT overwrite pays off.
            // Using printf here ensures the exploit only triggers when requested.
            printf(chemical_x); 
            print_str("\nSynthesis complete.\n");
        }
        else {
            print_str("[MOJO JOJO]: I shall return! FAREWELL!\n");
            exit(0);
        }
    }
    return 0;
}
