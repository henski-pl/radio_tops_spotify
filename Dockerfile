FROM python:3.11.1-alpine3.17

RUN mkdir /app

COPY radio_tops /app/radio_tops
COPY run.py /app

WORKDIR /app

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/app" \
    --no-create-home \
    --uid "5000" \
    "app"

RUN chown app:app /app -R

USER app

RUN pip install -r /app/radio_tops/requirements.txt

ENTRYPOINT ["python", "/app/run.py"]