FROM ubuntu:22.04

# Install minimal packages
RUN apt-get update && \
    apt-get install -y socat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create non-privileged user (no shell, no home directory)
RUN useradd -r -s /bin/false -M ctfuser

WORKDIR /challenge

# Copy challenge files
COPY challenge .
COPY flag.txt .

# Set secure permissions
RUN chown root:root challenge flag.txt && \
    chmod 755 challenge && \
    chmod 444 flag.txt && \
    # Ensure binary doesn't have dangerous capabilities
    setcap -r challenge 2>/dev/null || true

# Drop to non-privileged user
USER ctfuser

# Run with socat
# Note: socat still runs as ctfuser, but executes challenge as ctfuser
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./challenge,su=ctfuser"]