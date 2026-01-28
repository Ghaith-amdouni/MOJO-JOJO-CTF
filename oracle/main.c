const char binsh[] = "/bin/sh";

// Force the compiler to actually use it
void* get_binsh() {
    return (void*)binsh;
}

// Syscall wrappers
long syscall_write(int fd, const void *buf, unsigned long count) {
    long ret;
    __asm__ volatile (
        "mov $1, %%rax\n"
        "syscall"
        : "=a"(ret)
        : "D"(fd), "S"(buf), "d"(count)
        : "rcx", "r11", "memory"
    );
    return ret;
}

long syscall_read(int fd, void *buf, unsigned long count) {
    long ret;
    __asm__ volatile (
        "mov $0, %%rax\n"
        "syscall"
        : "=a"(ret)
        : "D"(fd), "S"(buf), "d"(count)
        : "rcx", "r11", "memory"
    );
    return ret;
}

void syscall_exit(int code) {
    __asm__ volatile (
        "mov $60, %%rax\n"
        "syscall"
        :
        : "D"(code)
    );
}

// Helper to print strings
void print(const char *s) {
    int len = 0;
    while(s[len]) len++;
    syscall_write(1, s, len);
}

// Our two gadgets
void echo_rax() {
    __asm__("pop %rax; ret;");
}

void echo_call() {
    __asm__("syscall; ret;");
}

// Vulnerable function
void listen() {
    char whisper[16];
    print("The void echoes...\n");
    syscall_read(0, whisper, 512);
}

// Entry point (no main, no libc)
void _start() {
    print("════════════════════════════════\n");
    print("          ECHOES \n");
    print("════════════════════════════════\n");
    print("In the silence, two sounds remain\n");
    print("Can you make them resonate?\n");
    print("════════════════════════════════\n\n");
    
    listen();
    
    print("\n  Silence returns...\n");
    syscall_exit(0);
}