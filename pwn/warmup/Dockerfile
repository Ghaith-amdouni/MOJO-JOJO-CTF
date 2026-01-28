FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y socat && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf

WORKDIR /app

COPY main .
COPY flag.txt .

RUN chmod +x main && \
    chmod 444 flag.txt && \
    chown root:root flag.txt main

USER ctf

EXPOSE 5000

CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:./main"]
