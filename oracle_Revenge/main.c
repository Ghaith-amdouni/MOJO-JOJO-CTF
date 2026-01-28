/*
 * Two Echoes - Part 2
 * 
 * Hardened: No /bin/sh string.
 * Vulnerability: Buffer Overflow.
 * Helper: Leaks address of a writable scratch buffer to facilitate Stack Pivoting.
 */

void syscall_exit(int code) {
    __asm__ volatile (
        "mov $60, %%rax\n"
        "syscall"
        : : "D"(code)
    );
}

long syscall_write(int fd, const void *buf, unsigned long count) {
    long ret;
    __asm__ volatile (
        "mov $1, %%rax\n"
        "syscall"
        : "=a"(ret) : "D"(fd), "S"(buf), "d"(count) : "rcx", "r11", "memory"
    );
    return ret;
}

long syscall_read(int fd, void *buf, unsigned long count) {
    long ret;
    __asm__ volatile (
        "mov $0, %%rax\n"
        "syscall"
        : "=a"(ret) : "D"(fd), "S"(buf), "d"(count) : "rcx", "r11", "memory"
    );
    return ret;
}

void print(const char *s) {
    int len = 0;
    while(s[len]) len++;
    syscall_write(1, s, len);
}

void print_hex(unsigned long addr) {
    char hex[19] = "0x";
    for(int i = 15; i >= 0; i--) {
        int nibble = (addr >> (i * 4)) & 0xF;
        hex[17 - i] = nibble < 10 ? '0' + nibble : 'a' + nibble - 10;
    }
    hex[18] = '\n';
    syscall_write(1, hex, 19);
}

// ════════════════════════════════════════
// GADGETS
// ════════════════════════════════════════
// Naked functions to ensure compiler doesn't add prologue/epilogue
__attribute__((naked)) void gadget_pop_rax() {
    __asm__ volatile ("pop %rax; ret;");
}

__attribute__((naked)) void gadget_syscall() {
    __asm__ volatile ("syscall; ret;");
}

// ════════════════════════════════════════
// SCRATCH BUFFER
// ════════════════════════════════════════
// A large writable area for stack pivoting
char scratch_buffer[0x1000] __attribute__((section(".data")));

void listen() {
    char buffer[32]; // Small buffer for overflow
    
    print("The void echoes louder...\n");
    print("Use this echo to guide your signal: ");
    print_hex((unsigned long)scratch_buffer);
    
    print("Speak signal:\n");
    // Overflow vulnerability
    syscall_read(0, buffer, 0x400); 
}

int main() {
    print("════════════════════════════════\n");
    print("     ECHOES Revenge\n");
    print("════════════════════════════════\n");
    print("Only signals remain.\n");
    print("════════════════════════════════\n");
    
    listen();
    
    print("\nThe silence returns.\n");
    syscall_exit(0);
    return 0;
}
