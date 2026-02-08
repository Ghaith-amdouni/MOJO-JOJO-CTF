FROM python:3.11-slim

WORKDIR /app

RUN useradd -m ctf

COPY server.py flag.txt ./
RUN chown -R root:ctf /app && chmod -R 750 /app

USER ctf

EXPOSE 1337

CMD ["python3", "server.py"]
