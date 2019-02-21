FROM python:3.6

COPY ./src /api
WORKDIR /api

RUN pip install -r requirements.txt

CMD ["python", "main.py"]