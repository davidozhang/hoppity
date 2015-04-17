# hoppity

Python3 implementations of RabbitMQ producer client and multi-threaded worker.

## Install

```python setup.py install```

## Usage

Using the client to send messages to your exchange and queue is easy. Launch python 3, and initialize the client:

```>>> from client import RabbitMQClient```

```>>> r = RabbitMQClient('PATH_TO_CLIENT_CONF_FILE')	# The path to your client configuration file is the parameter```

```>>> r.send_message('hello world')```

To launch a pool of RabbitMQ/Eventlet workers, run the following:
```python worker.py -c/--configuration PATH_TO_WORKER_CONF_FILE```

## Client Configuration File

Mandatory configuration parameters are:
* hostname
* username
* password
* vhost
* queue
* exchange

Optional configuration parameters are:
* durable_queue 		(default True)
* auto_delete_queue		(default False)
* exchange_type			(default fanout)
* durable_exchange 		(default True)
* auto_delete_exchange	(default False)
* timeout				(default None)

## Worker Configuration File

Mandatory configuration parameters are:
* hostname
* username
* password
* vhost
* queue

Optional configuration parameters are:
* num_threads 	(default 1000)
* timeout 		(default None)

num_threads and timeout should be a positive integer.

Use ' = ' as the separator between the parameter and your value.
