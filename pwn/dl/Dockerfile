FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    gcc \
    make \
    libseccomp-dev \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Add user
RUN useradd -m pwn

WORKDIR /home/pwn

COPY absolute_zero.c .
COPY server.c .
COPY Makefile Makefile
COPY flag.txt .

# Compile
RUN make

# Permissions
RUN chown -R root:pwn /home/pwn
RUN chmod -R 750 /home/pwn
RUN chmod 440 flag.txt

USER pwn

EXPOSE 1337

CMD ["./absolute_zero"]
