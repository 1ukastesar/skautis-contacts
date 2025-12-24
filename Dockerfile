#syntax=docker/dockerfile:1

FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN git config --global --add safe.directory /app

# Create necessary directories
RUN mkdir -p static/input static/output

CMD ["python3", "app.py"]
