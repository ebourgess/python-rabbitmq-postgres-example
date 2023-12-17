# ESS metered values monitoring and processing

> **NOTE:** Due to the limitations of Localstack and it's just running docker containers for the services, I just decided to bypass it here and use Docker containers instead. However, I will provide below a small infrastructure example that can be used on AWS.

## Introduction

The following project is an AWS app that:
- simulates sources for metered electricity data,
- transfers that data via a broker to a simulated business logic,
- and writes the results (in Kilowatts kW) to a DB.

## Directory Structure

```bash
├── README.md
├── consumer
│   ├── Dockerfile
│   ├── README.md
│   ├── app.py
│   └── requirements.txt
└── simulator
    ├── Dockerfile
    ├── README.md
    ├── app.py
    └── requirements.txt

2 directories, 9 files
```

## Technologies used

- Docker
- RabbitMQ for message brokering
- Postgresql for the Database

## How it works
- [Simulator](simulator/README.md)
- [Consumer/Business-Logic](consumer/README.md)

## Potential AWS Infrastructure 
- [Amazon RDS for PostgreSQL](https://aws.amazon.com/rds/postgresql/)
- [Amazon MQ for RabbitMQ](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/working-with-rabbitmq.html)
- Simulator and Consumer can be run each on a single instance of [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/)

