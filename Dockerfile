FROM python:3.11

COPY . /weather_bot

WORKDIR /weather_bot

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "run.py"]