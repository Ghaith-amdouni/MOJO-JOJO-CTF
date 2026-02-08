#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define LYRIC_SIZE 0x100
#define MAX_TRACKS 10

// ANSI color codes
#define RST   "\033[0m"
#define BLD   "\033[1m"
#define CYN   "\033[36m"
#define MAG   "\033[35m"
#define WHT   "\033[37m"
#define BCYN  "\033[96m"
#define BMAG  "\033[95m"
#define BGRN  "\033[92m"
#define BYLW  "\033[93m"
#define YLW   "\033[33m"
#define DIM   "\033[2m"

// Secure centralized storage
struct studio_t {
    char isolation1[4096];
    void *tracks[MAX_TRACKS];
    char isolation2[4096];
} __attribute__((aligned(64)));

struct studio_t studio = {.isolation1 = {1}, .isolation2 = {1}};

void banner() {
    printf("\n");
    printf(BLD BMAG "    ██╗  ██╗██╗██████╗     ██╗  ██╗ ██████╗ ██████╗ \n" RST);
    printf(BLD MAG  "    ██║  ██║██║██╔══██╗    ██║  ██║██╔═══██╗██╔══██╗\n" RST);
    printf(BLD BCYN "    ███████║██║██████╔╝    ███████║██║   ██║██████╔╝\n" RST);
    printf(BLD CYN  "    ██╔══██║██║██╔═══╝     ██╔══██║██║   ██║██╔═══╝ \n" RST);
    printf(BLD BYLW "    ██║  ██║██║██║         ██║  ██║╚██████╔╝██║     \n" RST);
    printf(BLD YLW  "    ╚═╝  ╚═╝╚═╝╚═╝         ╚═╝  ╚═╝ ╚═════╝ ╚═╝     \n" RST);
    printf(DIM WHT  "              [ S T U D I O   M A N A G E R ]\n" RST);
    printf("\n");
}

void mic_check() {
    asm("nop; nop; nop; nop;");
    printf(BLD BGRN "\n[+] Master Access Token Accepted!\n" RST);
    printf(CYN "    Retrieving secret flag...\n" RST);
    system("/bin/cat flag.txt");
    exit(0);
}

int get_int() {
    char buf[16];
    if (fgets(buf, 15, stdin) == NULL) return -1;
    return atoi(buf);
}

void add_track() {
    int i;
    for (i = 0; i < MAX_TRACKS; i++) if (studio.tracks[i] == NULL) break;
    if (i == MAX_TRACKS) return;
    studio.tracks[i] = malloc(LYRIC_SIZE);
    printf(BGRN "[+] " WHT "Track " BYLW "%d" WHT " loaded at %p\n" RST, i, studio.tracks[i]);
}

void delete_track() {
    printf(CYN "[?] " WHT "Idx: " RST);
    int idx = get_int();
    if (idx < 0 || idx >= MAX_TRACKS || studio.tracks[idx] == NULL) return;
    free(studio.tracks[idx]);
    studio.tracks[idx] = NULL;
    printf(YLW "[*] " WHT "Dropped\n" RST);
}

void edit_lyrics() {
    printf(CYN "[?] " WHT "Idx: " RST);
    int idx = get_int();
    if (idx < 0 || idx >= MAX_TRACKS || studio.tracks[idx] == NULL) return;
    printf(CYN "[>] " WHT "Lyrics: " RST);
    // Large enough overflow for Tcache Poisoning
    read(0, studio.tracks[idx], LYRIC_SIZE + 0x24); 
    printf(BGRN "[+] " WHT "Recorded\n" RST);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    banner();
    printf(DIM WHT "[*] Console ready at " BCYN "0x%zx" RST "\n", (size_t)&studio.tracks);
    while (1) {
        printf("\n 1.Add 2.Drop 3.Edit 4.Exit >> ");
        int choice = get_int();
        if (choice == 1) add_track();
        else if (choice == 2) delete_track();
        else if (choice == 3) edit_lyrics();
        else if (choice == 4) break;
    }
    return 0;
}
