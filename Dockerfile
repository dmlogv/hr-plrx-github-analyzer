FROM python:3.6-alpine3.6

COPY . /repoanalyzer
WORKDIR /repoanalyzer

ENTRYPOINT ["python", "analyzerepo"]