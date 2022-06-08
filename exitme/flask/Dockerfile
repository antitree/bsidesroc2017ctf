FROM ubuntu:22.04
MAINTAINER antitree "antitree at gmail"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential redis-server
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
