ARG FROM_IMAGE="ubuntu:22.04"

FROM ${FROM_IMAGE}

RUN apt-get update && apt-get install -y \
    socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /challenge

COPY challenge .
COPY flag.txt .

RUN chmod +x challenge

EXPOSE 1337

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./challenge"]
