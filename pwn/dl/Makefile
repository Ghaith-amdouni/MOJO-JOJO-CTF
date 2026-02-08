all:
	# Compile absolute_zero as an object file first if needed or just compile together
	# We compile server.c and absolute_zero.c together into the final binary 'absolute_zero'
	# Note: server.c has main(), absolute_zero.c has challenge()
	gcc -fstack-protector-all -no-pie -Wl,-z,relro,-z,lazy -o absolute_zero server.c absolute_zero.c -lseccomp

clean:
	rm -f absolute_zero
