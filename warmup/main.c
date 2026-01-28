#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void vuln() {
    char buffer[64];
    
    printf("Welcome to the warmup challenge!\n");
    printf("Enter your input: ");
    fflush(stdout);
    
    int n = read(0, buffer, 200);
    
    // Check that all bytes read are null (only check up to buffer size or n, whichever is smaller)
    int check_size = (n < 64) ? n : 64;
    for (int i = 0; i < check_size; i++) {
        if (buffer[i] != 0) {
            exit(1);
        }
    }
    
    printf("Good job!\n");
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    vuln();
    system("cat flag.txt");
    return 0;
}