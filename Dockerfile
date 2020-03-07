FROM python:3.7-alpine

ENV FLASK_APP flaskblog.py
ENV FLASK_CONFIG docker

RUN adduser -D flaskblog
USER flaskblog

WORKDIR /home/flaskblog

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY flaskblog.py config.py boot.sh ./

# runtime configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]