FROM python:3.13
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install

WORKDIR /blog
COPY requirements.txt /blog/
COPY .env-example /blog/.env
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /blog/

ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]