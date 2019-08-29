`gpio_httpd` is a simple web server to control Raspberry Pi GPIO pins. Example use case is activating a relay

```
$ pip install -r requirements.txt
$ python gpio_httpd.py
```

Running `curl -X POST http://localhost/17/low?ms=250` will set pin 17 to GPIO.LOW for 250 milliseconds

### Docker

`docker run --device "/dev/gpiomem" -p "80:80" bakerba/gpio_httpd`

### Docker Compose

```
version: '3.3'

services:
  gpio_httpd:
    image: bakerba/gpio_httpd
    container_name: gpio_httpd
    devices:
      - "/dev/gpiomem"
    ports:
      - "80:80"
```

### Usage

```
$ python gpio_httpd.py --help

usage: gpio_httpd.py [-h] [--debug] [--port PORT]

optional arguments:
  -h, --help           show this help message and exit
  --debug              enable debug logging
  --port PORT          port
```
