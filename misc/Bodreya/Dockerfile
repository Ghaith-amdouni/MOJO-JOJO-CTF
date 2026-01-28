FROM python:3.9-slim

# Install dependencies (system)
RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*
ENV PYTHONUNBUFFERED=1

# Install python dependencies
RUN pip install hilbertcurve

WORKDIR /app

COPY server.py .

# Create a non-root user
RUN useradd -m ctf
USER ctf

# Using socat is optional if using python threading, but python threading is fine for this scale.
# However, usually CTF challenges run one process per connection or handle it internally.
# The current server.py uses threading. It's fine.
CMD ["python", "server.py"]

EXPOSE 1337
