FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && \
    apt-get install -y socat gcc && \
    rm -rf /var/lib/apt/lists/*

# Create user for security
RUN useradd -m ctf

WORKDIR /app

# Copy binary and flag
COPY main .
COPY flag.txt .

# Set permissions
RUN chmod +x main && \
    chmod 444 flag.txt && \
    chown root:root flag.txt main

# Expose port
EXPOSE 5000

# Run with socat
USER ctf
CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:./main,stderr"]
