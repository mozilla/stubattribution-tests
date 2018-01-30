FROM python:2.7-alpine
WORKDIR /src
RUN pip install pipenv
COPY Pipfile Pipfile.lock /src/
RUN pipenv install --system --skip-lock --deploy
COPY . /src
CMD pytest --driver SauceLabs \
  --capability browserName Chrome \
  --capability platform "Windows 10"
