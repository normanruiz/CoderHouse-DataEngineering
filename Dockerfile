FROM python:3.10-slim

RUN mkdir /opt/asteroides-etl
RUN mkdir /opt/asteroides-etl/Modelo
RUN mkdir /opt/asteroides-etl/Servicio

WORKDIR /opt/asteroides-etl

COPY Modelo ./Modelo
COPY Servicio ./Servicio
COPY app.py config.xml requirements.txt ./

RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3","-u","app.py"]