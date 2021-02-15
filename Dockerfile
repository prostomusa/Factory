FROM python:3.8.5-alpine
# set work directory
WORKDIR /usr/src/Factory
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
COPY ./req.txt .
RUN pip install -r req.txt
# copy project
COPY . .