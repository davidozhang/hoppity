# -*- coding: utf-8 -*-

from amqplib import client_0_8 as amqp

from configuration import Configuration


class RabbitMQClient(object):
    def __init__(self, path):
        try:
            self.configs = self.get_configs(path)
            self.conn = amqp.Connection(
                host=self.configs['hostname'],
                userid=self.configs['username'],
                password=self.configs['password'],
                virtual_host=self.configs['vhost'],
                connect_timeout=self.configs['timeout'],
                insist=False,
            )
            self.channel = self.conn.channel()
            self.exchange = self.configs['exchange']
            self.queue = self.configs['queue']
            self.create_exchange()
            self.create_and_bind_queue()
        except OSError:
            print ('Cannot establish connection to RabbitMQ.')

    def send_message(self, msg):
        try:
            message = amqp.Message(msg)
            message.properties['content_type'] = 'text/plain'
            message.properties['delivery_mode'] = 2
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key='',
                msg=message,
            )
        except AttributeError:
            raise Exception('Please initialize RabbitMQClient properly.')

    def create_and_bind_queue(self):
        try:
            self.channel.queue_declare(
                queue=self.queue,
                durable=self.configs['durable_queue'],
                auto_delete=self.configs['auto_delete_queue'],
            )
            self.channel.queue_bind(queue=self.queue, exchange=self.exchange)
        except:
            raise Exception('Cannot create/bind queue.')

    def create_exchange(self):
        try:
            self.channel.exchange_declare(
                exchange=self.exchange,
                type=self.configs['exchange_type'],
                durable=self.configs['durable_exchange'],
                auto_delete=self.configs['auto_delete_exchange'],
            )
        except:
            raise Exception('Cannot create exchange.')

    def close(self):
        self.channel.close()
        self.conn.close()

    def get_configs(self, path):
        c = Configuration(path=path)
        c.required = {
            'hostname',
            'username',
            'password',
            'vhost',
            'exchange',
            'queue',
        }
        c.accepted = {
            'durable_queue',
            'auto_delete_queue',
            'exchange_type',
            'durable_exchange',
            'auto_delete_exchange',
            'timeout',
        }
        if not c.read():
            raise Exception('Configuration file not set properly.')
        configs = c.result

        if 'durable_queue' in configs:
            configs['durable_queue'] = bool(configs['durable_queue'])
        else:
            configs['durable_queue'] = True

        if 'auto_delete_queue' in configs:
            configs['auto_delete_queue'] = bool(configs['auto_delete_queue'])
        else:
            configs['auto_delete_queue'] = False

        if 'exchange_type' not in configs:
            configs['exchange_type'] = 'fanout'

        if 'durable_exchange' in configs:
            configs['durable_exchange'] = bool(configs['durable_exchange'])
        else:
            configs['durable_exchange'] = True

        if 'auto_delete_exchange' in configs:
            configs['auto_delete_exchange'] = bool(configs['auto_delete_exchange'])
        else:
            configs['auto_delete_exchange'] = False

        if 'timeout' in configs:
            configs['timeout'] = int(configs['timeout'])
        else:
            configs['timeout'] = None

        return configs
