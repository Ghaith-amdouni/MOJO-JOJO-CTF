CC=gcc
CFLAGS=-lseccomp

all: challenge

challenge: challenge.c
	$(CC) -o challenge challenge.c $(CFLAGS)

clean:
	rm -f challenge
