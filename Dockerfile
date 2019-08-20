FROM alpine:latest

RUN \
 apk add curl && \
 curl -L https://github.com/balena-io/qemu/releases/download/v3.0.0%2Bresin/qemu-3.0.0+resin-arm.tar.gz | tar --strip=1 -zxvf -

FROM balenalib/rpi-debian-python:3.7.2

COPY --from=0 /qemu-arm-static /usr/bin

RUN apt-get update && apt-get install -y gcc libc-dev

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY gpio_httpd.py .

ENTRYPOINT ["./gpio_httpd.py"]
