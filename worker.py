# -*- coding: utf-8 -*-

import json
import argparse
import eventlet

from configuration import Configuration

eventlet.monkey_patch()


class RabbitMQWorker(object):
    def __init__(self, **kwargs):
        self.configs = kwargs
        self.conn = amqp.Connection(
            host=self.configs['host'],
            userid=self.configs['user'],
            password=self.configs['password'],
            virtual_host=self.configs['vhost'],
            connect_timeout=self.configs['timeout'],
            insist=False,
        )
        self.channel = self.conn.channel()
        self.consume()

    def handle(self, delivery_tag, body):
        msg = json.loads(body)

        # Do something with the received msg HERE!

        self.channel.basic_ack(delivery_tag=delivery_tag)
        return response

    def consume(self):
        msg = self.channel.basic_get(queue=self.configs['queue'])
        if msg:
            self.handle(msg.delivery_tag, msg.body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=('Create a pool of RabbitMQ/Eventlet workers.'),
    )
    parser.add_argument(
        '-c',
        '--configuration',
        help='Specify the path to the worker.conf file.',
        required=True,
    )
    args = vars(parser.parse_args())

    c = Configuration(path=args['configuration'])
    c.required = {
        'hostname',
        'username',
        'password',
        'vhost',
        'queue',
    }
    c.accepted = {
        'num_threads',
        'timeout',
    }
    if not c.read():
        raise Exception('Configuration file not set properly.')
    configs = c.result

    if 'timeout' in configs:
        configs['timeout'] = int(configs['timeout'])
    else:
        configs['timeout'] = None

    if 'num_threads' in configs:
        num_threads = int(configs['num_threads'])
        pool = eventlet.GreenPool(size=int(configs['num_threads']))
    else:
        num_threads = 1000
        pool = eventlet.GreenPool()

    try:
        while True:
            for i in range(num_threads):
                pool.spawn(
                    RabbitMQWorker,
                    host=configs['hostname'],
                    user=configs['username'],
                    password=configs['password'],
                    vhost=configs['vhost'],
                    timeout=configs['timeout'],
                    queue=configs['queue'],
                )
            pool.waitall()
    except:
        print ('RabbitMQ/Eventlet Worker has terminated.')
