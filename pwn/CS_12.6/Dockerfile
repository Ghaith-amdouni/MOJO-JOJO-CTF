FROM ubuntu:22.04

# Install minimal packages
RUN apt-get update && \
    apt-get install -y socat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN useradd -r -s /bin/false -M ctfuser

WORKDIR /challenge

# Copy challenge files
COPY challenge .
COPY flag.txt .

# Set secure permissions
RUN chown root:root challenge flag.txt && \
    chmod 755 challenge && \
    chmod 444 flag.txt && \
    setcap -r challenge 2>/dev/null || true

# Run with socat as root, it will drop to ctfuser per connection

# Run with socat
# Note: socat still runs as ctfuser, but executes challenge as ctfuser
CMD ["socat", "-T60", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./challenge,su=ctfuser,stderr"]