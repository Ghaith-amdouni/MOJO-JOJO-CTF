FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    gdb \
    python3 \
    gcc \
    socat \
    && rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -m ctf

WORKDIR /home/ctf

# Copy challenge files
COPY target.c .
COPY jail.py .
COPY gdbinit .

# Compile target
# -no-pie: Easier to find addresses (though GDB resolves symbols anyway)
# -g: Include debug info so GDB is nice to use
RUN gcc -o target target.c -no-pie -g

# Create flag
# "do you know what gdb stands for go down bitch!!!!!!" -> Inspired flag
RUN echo "MOJO-JOJO{G0_D0wn_B1tch_D1r3ct_M3m0ry_Ex3cut10n_1s_K1ng}" > flag.txt

# Permissions
RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    chmod 740 flag.txt

# Start script
RUN echo '#!/bin/bash\n\
    gdb -nx -q -x /home/ctf/gdbinit ./target\n\
    ' > /home/ctf/start.sh && chmod +x /home/ctf/start.sh

USER ctf

# Expose port (if needed for remote, though this is usually wrapped by socat in the infra)
# We will use socat here for testing
CMD socat TCP-LISTEN:1339,reuseaddr,fork EXEC:"/home/ctf/start.sh"
