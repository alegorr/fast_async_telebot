FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY ./deploy/ztest.online/nginx/nginx.conf /etc/nginx/conf.d/

RUN mkdir -p /root/ssl
COPY ./deploy/ztest.online/cert/cert1.pem /root/ssl/cert.pem
COPY ./deploy/ztest.online/cert/privkey1.pem /root/ssl/key.pem

RUN mkdir /code
WORKDIR /code

EXPOSE 80
EXPOSE 443


FROM python:3.10.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
RUN mkdir /static

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

COPY . /code/
WORKDIR /code

EXPOSE 8000
