# ESS metered values monitoring and processing
## Consumer/Business-Logic

### Directory structure 

```bash
.
├── Dockerfile
├── README.md
├── app.py
└── requirements.txt

0 directories, 4 files
```

### Database Requirements

- Create a database called `ess` in Postgres using the following query

```sql
CREATE DATABASE ess;
```

- Connect to the database `ess` by running `\c ess` and then run the following query

```sql
CREATE TABLE ess (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    load_sum NUMERIC(10, 2) NOT NULL,
    battery_load NUMERIC(10, 2) NOT NULL,
    site_load NUMERIC(10, 2) NOT NULL
);
```

### Requirements to run it

- Create a `.env` file with the following values
```
HOST=host.docker.internal
POSTGRES_PORT=5432
RABBITMQ_PORT=5672
POSTGRES_DB_NAME=ess
POSTGRES_USER=postgres
POSTGRES_PASSWORD=example
```

- Create `docker` image 
```bash
docker build -t consumer .
```

### How it works

The file `app.py` holds the code for the consumer/business logic here. It has two main functions here:
- `consume_message`, it's  a callback function that is designed to be called when a message is received from a RabbitMQ queue, here's how it mainly works:
    - It parses the body of the message as JSON using `json.loads(body)`. he message is expected to be a dictionary with at least two keys: `data_source` and `value`.
    - It checks the `data_source`, if it's `site` then it updates the `site_value` variable with the `value` of the message
    - If the `data_source` is `battery`, it calculates `load_sum` as the sum of the `value` from the `message` and `site_load`. It then calls the `add_to_database` function to insert a new record into the `ess` table in the PostgreSQL database. The record includes the current timestamp, `load_sum`, the `value` from the message (which is the battery load), and `site_load`. After adding the record, it resets `site_load` to 0.
    - If an error occurs during the processing of the message (for example, if the message body cannot be parsed as JSON, or if the `data_source` field is not `site` or `battery`), it catches the exception and prints an error message to the console.

- `add_to_database`, this function is used to insert a new record into the `ess` table in the PostgreSQL database. The record includes the current timestamp, `load_sum`, the `battery_load`, and `site_load`.

