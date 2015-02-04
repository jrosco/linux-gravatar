#!/usr/bin/env python

""" Supports python2 and python3"""
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

import os
import platform
import logging


class GravatarSettings:

    def __init__(self, section, location):

        logging.basicConfig(level=logging.DEBUG)
        self.section = section
        self.location = location

    def read_config(self, key):

        value = None
        try:
            config = configparser.ConfigParser()
            config.read(self.location)
            value = config.get(self.section, key)
        except:
            logging.error('couldn\'t find correct setting details, '
                          'creating new file')
            self.write_config_file(self.location)

        return value

    def read_config_bool(self, key):

        bool_value = False
        try:
            config = configparser.ConfigParser()
            config.read(self.location)
            bool_value = config.getboolean(self.section, key)
        except RuntimeError as e:
            logging.error(e)

        return bool_value

    def save_to_config(self, key, value):

        try:
            config = configparser.ConfigParser()
            config.read(self.location)

            if self.section not in config.sections():
                config.add_section(self.section)

            config.set(self.section, key, value)
            with open(self.location.encode(), 'w') as cf:
                config.write(cf)
        except RuntimeError as e:
            logging.debug(e)

    @staticmethod
    def write_config_file(location):

        cfgfile = open(location.encode(), 'w')
        config = configparser.ConfigParser()
        config.add_section('Settings')
        config.set('Settings', 'username', '')
        config.set('Settings', 'email', '')
        config.set('Settings', 'check', '60.0')
        config.set('Settings', 'notifications', 'False')
        config.set('Settings', 'startup', 'False')
        config.write(cfgfile)
        cfgfile.close()


def settings_location():

        linux_os = 'linux'
        windows_os = 'windows'
        home_path = None
        os_type = platform.system()

        if os_type.lower() == linux_os:
            home_path = os.path.expanduser('~')
        elif os_type.lower() is windows_os:
            home_path = os.path.expanduser('~')
        else:
            home_path = os.path.expanduser('~')
            logging.error('Unknown OS')

        file_path = home_path + '/.gravatar_settings.cfg'

        if not os.path.isfile(file_path):
            try:
                open(file_path, 'a').close()
                GravatarSettings('Settings', file_path).write_config_file(file_path)
            except RuntimeError as e:
                logging.error(e)
        else:
            pass

        return file_path