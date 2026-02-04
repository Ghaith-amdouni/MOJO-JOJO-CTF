FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Add a non-root user
RUN useradd -m ctf

WORKDIR /home/ctf

COPY main .
COPY flag.txt .

# Set strict permissions
RUN chown -R root:root /home/ctf && \
    chmod 755 /home/ctf && \
    chmod 444 flag.txt && \
    chmod 555 main

USER ctf
EXPOSE 5000

CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:./main"]
