# ESS metered values monitoring and processing
## Simulator

### Directory structure 

```bash
.
├── Dockerfile
├── README.md
├── app.py
└── requirements.txt

0 directories, 4 files
```

### Requirements to run it
- Create a `.env` file with the following values
```
HOST=host.docker.internal
PORT=5672
```

- Create `docker` image 
```bash
docker build -t simulator .
```

### How it works

The file `app.py` contains the code for this simulator.
The function `simulate_meter` is a simulation of a meter that generates random values within a specified range (min_val, max_val) at regular intervals (delay). It's designed to run indefinitely in a loop.

Here's a step-by-step breakdown:

1. The function enters an infinite loop with `while True`.
2. Inside the loop, it generates a random floating-point number between `min_val` and `max_val`, rounded to one decimal place.
3. It then creates a message in the form of a dictionary. This message contains the generated value, the current timestamp, and the data source name.
4. The message is then published to a RabbitMQ queue named 'ess_queue' using the `basic_publish` method of the `channel` object. The message dictionary is converted to a JSON string before being sent.
5. The function prints a message to the console indicating what data has been sent.
6. The function then pauses for a specified number of seconds (the `delay` parameter) before the next iteration of the loop.

This function is designed to be run in a separate process, as indicated by the `Process` calls later in the code. This allows multiple meters to be simulated concurrently.