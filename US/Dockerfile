FROM python:3.5

RUN apt-get update && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN groupadd -g 799 nyu && useradd -r -u 999 -g nyu nyu

WORKDIR /app

RUN pip install Flask requests
USER nyu

COPY --chown=nyu:nyu . .

CMD ["python", "./user_server.py"]