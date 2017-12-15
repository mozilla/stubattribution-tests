FROM python:2.7-alpine
RUN apk add --update git openssl
WORKDIR /src
COPY requirements /src/requirements/
RUN pip install -r requirements/tests.txt
RUN pip install -r requirements/flake8.txt
COPY . /src
CMD pytest --driver=SauceLabs \
    --capability browserName Chrome \
    --capability platform "Windows 10" \
    --junit-xml=results/py27.xml \
    --html=results/py27.html --self-contained-html \
    --log-raw=results/py27_raw.txt \
    --log-tbpl=results/py27_tbpl.txt
