FROM python:3.7-alpine3.7

COPY . /repoanalyzer
WORKDIR /repoanalyzer

ENTRYPOINT ["python", "analyzerepo"]