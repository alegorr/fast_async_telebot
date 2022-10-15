FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY web/nginx.conf /etc/nginx/conf.d/
RUN mkdir -p /root/ssl
COPY ./cert/ztest.online/cert1.pem /root/ssl/cert.pem
COPY ./cert/ztest.online/privkey1.pem /root/ssl/key.pem
RUN mkdir /code
WORKDIR /code
EXPOSE 80

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
