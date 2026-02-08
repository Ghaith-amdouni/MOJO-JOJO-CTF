CFLAGS = -pie -fPIE -fstack-protector-all -Wl,-z,relro -Wl,-z,lazy -o hiphop

all: hiphop

hiphop: hiphop.c
	gcc $(CFLAGS) hiphop.c

clean:
	rm -f hiphop
