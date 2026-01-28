FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    socat \
    gcc \
    libseccomp-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /challenge

COPY challenge.c .
COPY flag.txt .

RUN gcc -o challenge challenge.c -lseccomp

EXPOSE 1337

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./challenge"]
