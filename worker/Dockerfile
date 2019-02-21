FROM python:3.6

COPY ./src /worker
WORKDIR /worker

RUN pip install -r requirements.txt
RUN chmod +x pooler.sh

CMD ["bash", "pooler.sh"]