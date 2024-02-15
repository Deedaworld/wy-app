FROM python:3
RUN mkdir -p /usr/src/app/ticket
WORKDIR /usr/src/app/ticket
COPY . .
RUN pip3 install flask
RUN pip3 install flask-cors
RUN pip3 install redis
RUN pip3 install boto3
CMD ["python3", "redis_py.py"]
