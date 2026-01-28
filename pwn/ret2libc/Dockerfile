FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf

WORKDIR /app

COPY main run
RUN chmod +x run

COPY flag.txt libc.so.6 ld-linux-x86-64.so.2 ./

USER ctf

EXPOSE 5000

CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:timeout 60 ./run,stderr"]
