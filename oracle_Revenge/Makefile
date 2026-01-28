CC=gcc
CFLAGS=-fno-stack-protector -no-pie -Wl,-z,relro,-z,now -O2 -fomit-frame-pointer

all: main

main: main.c
	$(CC) $(CFLAGS) -o main main.c

clean:
	rm -f main
