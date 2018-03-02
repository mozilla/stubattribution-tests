FROM python:2.7
WORKDIR /src

RUN pip install pipenv
COPY Pipfile /src/
RUN pipenv install --system --skip-lock
COPY . /src

CMD pytest --driver SauceLabs \
  --capability browserName Chrome \
  --capability platform "Windows 10"
