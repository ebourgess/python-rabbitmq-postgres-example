FROM python:3.10-slim-bookworm
WORKDIR /app

ADD . /app

# This is needed for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "app.py" ]