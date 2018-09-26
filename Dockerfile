FROM python:2.7
WORKDIR /src

COPY Pipfile pipenv.txt /src/
RUN pip install --upgrade pip -r pipenv.txt
RUN pipenv install --system --skip-lock
COPY . /src

CMD pytest --driver SauceLabs \
  --capability browserName Chrome \
  --capability platform "Windows 10"
