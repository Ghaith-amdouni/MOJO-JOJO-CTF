FROM ubuntu:18.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    socat \
    && rm -rf /var/lib/apt/lists/*

# Create challenge user
RUN useradd -m ctf

WORKDIR /home/ctf

# Copy challenge files
COPY hiphop.c Makefile flag.txt /home/ctf/

# Build the binary with no PIE for easier exploitation, partial RELRO for GOT overwrite
RUN make

# Set permissions
RUN chown -R root:ctf /home/ctf && \
    chmod 755 /home/ctf/hiphop && \
    chmod 444 /home/ctf/flag.txt

# Exposure
EXPOSE 9008

# Start the service
USER ctf
CMD ["socat", "TCP-LISTEN:9008,reuseaddr,fork", "EXEC:./hiphop,stderr"]
