# -*- coding: utf-8 -*-
import os
import configparser

from letoh import logger


XDG_CONFIG_HOME = os.environ.get('XDG_CONFIG_HOME',
                                 os.path.expanduser('~/.config'))
APP_NAME = 'harbour-pyletoh'
APP_CONFIG_DIR = os.path.join(XDG_CONFIG_HOME, APP_NAME)
APP_CONFIG_PATH = os.path.join(APP_CONFIG_DIR, APP_NAME + '.cfg')


def init():
    if not os.path.exists(APP_CONFIG_DIR):
        logger.info('Creating {0:s}'.format(APP_CONFIG_DIR))
        os.makedirs(APP_CONFIG_DIR)

    config = configparser.ConfigParser()
    config['default'] = {'color': '#FF0000'}
    with open(APP_CONFIG_PATH, 'w') as fp:
        config.write(fp)


def load():
    if not os.path.exists(APP_CONFIG_PATH):
        logger.info('Creating {0:s}'.format(APP_CONFIG_PATH))
        init()

    config = configparser.ConfigParser()
    config.read(APP_CONFIG_PATH)
    return config


def save(config):
    if not os.path.exists(APP_CONFIG_DIR):
        logger.info('Creating {0:s}'.format(APP_CONFIG_PATH))
        os.makedirs(APP_CONFIG_DIR)

    with open(APP_CONFIG_PATH, 'w') as fp:
        config.write(fp)
