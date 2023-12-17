FROM python:3.10-slim-bookworm

WORKDIR /app

ADD . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "app.py" ]