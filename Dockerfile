FROM python:2.7-alpine
RUN apk add --update git openssl
WORKDIR /src
COPY requirements /src/requirements/
RUN pip install -r requirements/tests.txt
RUN pip install -r requirements/flake8.txt
COPY . /src
CMD pytest --driver SauceLabs \
  --capability browserName Chrome \
  --capability platform "Windows 10"
