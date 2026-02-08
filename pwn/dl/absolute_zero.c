#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/prctl.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
#include <stddef.h>

void install_seccomp() {
    struct sock_filter filter[] = {
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, (offsetof(struct seccomp_data, arch))),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, (offsetof(struct seccomp_data, nr))),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 0, 6, 0),   // read
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 1, 5, 0),   // write
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 257, 4, 0), // openat
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 15, 3, 0),  // rt_sigreturn
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 60, 2, 0),  // exit
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 231, 1, 0), // exit_group
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    };
    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
        .filter = filter,
    };
    prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
    prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
}

void process_input() {
    char buf[64];
    // No leaks. Pure Blind.
    read(0, buf, 1024); 
}

void gadgets() {
    asm("pop %rdi; ret");
    asm("pop %rsi; ret");
    asm("pop %rdx; ret");
    asm("pop %rax; ret");
    asm("syscall; ret");
}

// Export challenge for server.c
void challenge() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    install_seccomp();
    process_input();
}
