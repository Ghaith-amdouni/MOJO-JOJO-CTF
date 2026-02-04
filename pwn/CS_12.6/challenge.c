#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <fcntl.h>

volatile void (*_k_dispatch_table)(long, long, long) __attribute__((used));

void _sys_maintenance(long a, long b, long c) {
    if (a != 0x1206 || b != 0x1161 || c != 0xcafebab) {
        printf("\x1b[31m[CRITICAL]\x1b[0m Unauthorized neural override detected. Vectors misaligned.\n");
        fflush(stdout);
        return;
    }
    
    printf("\n\x1b[32m[SYSTEM]\x1b[0m Quantum Vector Alignment Confirmed.\n");
    printf("\x1b[32m[SYSTEM]\x1b[0m Bypassing security kernels... Initiating Core Dump...\n\n");
    fflush(stdout);
    
    int fd = open("flag.txt", O_RDONLY);
    if (fd < 0) {
        write(1, "[ERROR] Flag sector not found.\n", 31);
        exit(1);
    }
    
    char flag[128];
    int n = read(fd, flag, sizeof(flag));
    if (n > 0) {
        write(1, "\x1b[33m>>> DATA EXFILTRATED:\x1b[0m ", 30);
        write(1, flag, n);
        write(1, "\n", 1);
    }
    close(fd);
    
    printf("\n\x1b[32m[SYSTEM]\x1b[0m Session terminated safely.\n");
    fflush(stdout);
    sleep(1);
    exit(0);
}

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

// Manual gadgets 
__attribute__((naked)) void _proc_ctx() {
    __asm__(
        ".global _proc_ctx_1\n"
        "_proc_ctx_1:\n"
        "pop %rbx\n"
        "pop %rbp\n"
        "pop %r12\n"
        "pop %r13\n"
        "pop %r14\n"
        "pop %r15\n"
        "ret\n"
        "nop\n"
        "nop\n"
        ".global _proc_ctx_2\n"
        "_proc_ctx_2:\n"
        "mov %r14, %rdx\n"
        "mov %r13, %rsi\n"
        "mov %r12d, %edi\n"
        "call *(%r15,%rbx,8)\n"
        "ret\n"
    );
}

void _log_handler() {
    // Shifting offsets: Add dummy variables to push canary and return address further down the stack
    long dummy[8] = {0xdeadbeef, 0xcafebabe, 0x13371337, 0x41414141};
    char buffer[20];
    
    printf("\n[LOG] Initializing secure logging sequence...\n");
    printf("[LOG] Identity verification required: ");
    
    // Vulnerability: Format String (Leads to Canary/PIE leak)
    // Limited buffer forces multiple leaks or clever tricks
    if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
        printf("[LOG] Identity confirmed: ");
        printf(buffer); 
    }
}

void _auth_guard() {
    char secure_phrase[32];
    printf("\n[GATE] Physical authentication barrier active.\n");
    printf("[GATE] Provide phrase: ");
    
    read(0, secure_phrase, 256); 
    
    printf("[GATE] Authentication failed. Terminating session.\n");
}

int main() {
    init();
    _k_dispatch_table = _sys_maintenance;
    
    printf("--- CS 12.06 ---\n");
    printf("Security Level: MAXIMUM\n");
    
    _log_handler();
    _auth_guard();
    
    printf("[SYSTEM] System shutdown.\n");
    return 0;
}
