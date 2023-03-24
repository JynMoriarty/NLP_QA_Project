FROM python:3.9.15

WORKDIR /app

ENV PYTHONUNBUFFERED=1


COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install gcc


COPY . /app

EXPOSE 8007

CMD ["python" ,"manage.py","runserver","0.0.0.0:80"]
