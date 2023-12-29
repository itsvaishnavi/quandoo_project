FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

FROM selenium/standalone-chrome:latest

USER root

RUN apt-get update && apt-get install -y python3 python3-pip

RUN apt-get install -y libmysqlclient-dev

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt



COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]