# -*- coding: utf-8 -*-
import os
import time
import contextlib
import configparser

from letoh import logger

XDG_CONFIG_HOME = os.environ.get('XDG_CONFIG_HOME',
                                 os.path.expanduser('~/.config'))
APP_NAME = 'harbour-pyletoh'
APP_CONFIG_DIR = os.path.join(XDG_CONFIG_HOME, APP_NAME)
APP_CONFIG_PATH = os.path.join(APP_CONFIG_DIR, APP_NAME + '.cfg')

CACHE = {}

_marker = object()


def cached(func):
    def getter(*args, **kwargs):
        key = func.__name__
        value = CACHE.get(key, _marker)
        if value is _marker or value[0] < int(time.time()) - 1:
            value = CACHE[key] = (int(time.time()), func(*args, **kwargs))
        return value[1]
    return getter


def init():
    if not os.path.exists(APP_CONFIG_DIR):
        logger.info('Creating {0:s}'.format(APP_CONFIG_DIR))
        os.makedirs(APP_CONFIG_DIR)

    config = configparser.ConfigParser(allow_no_value=True)
    config['DEFAULT'] = {'color': '#ff0000'}

    with open(APP_CONFIG_PATH, 'w') as fp:
        config.write(fp)


def migrate(config):
    if config.has_section('default'):
        config['DEFAULT'] = dict(config.items('default'))
        config.remove_section('default')
    save(config)


@cached
def load():
    if not os.path.exists(APP_CONFIG_PATH):
        logger.info('Creating {0:s}'.format(APP_CONFIG_PATH))
        init()

    config = configparser.ConfigParser(allow_no_value=True)
    config.read(APP_CONFIG_PATH)

    if config.has_section('default'):
        migrate(config)

    return config


def save(config):
    if not os.path.exists(APP_CONFIG_DIR):
        logger.info('Creating {0:s}'.format(APP_CONFIG_DIR))
        os.makedirs(APP_CONFIG_DIR)

    with open(APP_CONFIG_PATH, 'w') as fp:
        config.write(fp)


@contextlib.contextmanager
def edit():
    settings = load()
    yield settings
    save(settings)


def save_defaults(**kwargs):
    with edit() as settings:
        for key, value in kwargs.items():
            settings.set('DEFAULT', key, value)
