FROM python:2.7-alpine
RUN apk add --update git openssl
WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt
COPY . /src
CMD pytest --driver SauceLabs \
  --capability browserName Chrome \
  --capability platform "Windows 10"
