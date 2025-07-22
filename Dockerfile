FROM python:3.12.11-slim

WORKDIR /app
COPY . /app

EXPOSE 8009

RUN apt-get update && \
    apt-get install -y make pkg-config gcc default-libmysqlclient-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN chmod -R 777 /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]