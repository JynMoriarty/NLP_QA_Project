FROM python:3.10-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV SECRET_KEY=${SECRET_KEY}
ENV credential=${credential}

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt


COPY . /app

EXPOSE 8007

CMD ["python" ,"manage.py","runserver","0.0.0.0:8001"]