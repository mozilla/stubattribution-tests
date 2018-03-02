FROM ubuntu:xenial
WORKDIR /src

RUN apt-get update \
  && apt-get install -y curl python2.7
RUN curl -fsSl https://bootstrap.pypa.io/get-pip.py | python2.7 \
  && pip install pipenv
COPY Pipfile /src/
RUN pipenv install --system --skip-lock
COPY . /src

CMD pytest --driver SauceLabs \
  --capability browserName Chrome \
  --capability platform "Windows 10"
