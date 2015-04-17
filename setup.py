# -*- coding: utf-8 -*-

from setuptools import setup


with open('requirements.txt') as fp:
    dependencies = [l.strip() for l in fp.readlines()]

setup(
    name='RabbitMQ',
    description='RabbitMQ',
    py_modules=['client', 'worker'],
    install_requires=dependencies,
)
