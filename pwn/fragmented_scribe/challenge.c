#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <ctype.h>
#include <seccomp.h>
#include <fcntl.h>

#define MAX_SHELLCODE_SIZE 1024

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void setup_seccomp() {
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL);
    if (ctx == NULL) exit(1);

    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(openat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);

    seccomp_load(ctx);
}

int validate_shellcode(unsigned char *code, size_t size) {
    for (size_t i = 0; i < size; i++) {
        if (code[i] < 32 || code[i] > 126) {
            return 0;
        }
    }
    return 1;
}

int main() {
    init();

    unsigned char *shellcode = mmap(NULL, MAX_SHELLCODE_SIZE, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (shellcode == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }

    printf("--- THE FRAGMENTED SCRIBE ---\n");
    printf("Provide your shellcode:\n");
    printf("> ");

    ssize_t n = read(0, shellcode, MAX_SHELLCODE_SIZE);
    if (n <= 0) exit(1);

    if (!validate_shellcode(shellcode, n)) {
        printf("[ERROR] Your incantation contains forbidden shadows. The scribe refuses to write such impurity.\n");
        exit(1);
    }

    printf("[SYSTEM] Sandboxing initiated... Good luck, scribe.\n");
    setup_seccomp();

    // Stub: pass shellcode address in R13 and clean most registers.
    __asm__ volatile (
        "mov %0, %%r13\n"
        "xor %%rax, %%rax\n"
        "xor %%rbx, %%rbx\n"
        "xor %%rcx, %%rcx\n"
        "xor %%rdx, %%rdx\n"
        "xor %%rsi, %%rsi\n"
        "xor %%rdi, %%rdi\n"
        "jmp *%%r13\n"
        :
        : "r" (shellcode)
        : "rax", "rbx", "rcx", "rdx", "rsi", "rdi", "r13"
    );

    return 0;
}
