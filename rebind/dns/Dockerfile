FROM python:2
COPY . /src
ENV PYTHONUNBUFFERED=0
RUN pip install -r /src/requirements.txt
CMD ["python", "/src/dns_server.py"]
