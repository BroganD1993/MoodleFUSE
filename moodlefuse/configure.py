#!/usr/bin/env python
# encoding: utf-8

"""Class to configure MoodleFUSE
"""

import os
import argparse
import getpass

from alembic import command
from ConfigParser import SafeConfigParser
from alembic.config import Config as AlembicConfig


def main():
    Configurer()


class Configurer(object):

    def __init__(self):
        config_folder = self._create_config_folder()
        database = self._create_user_database()
        self._create_configuration(config_folder)
        self._create_filesystem_folder()
        self._create_file_cache()

    def _create_config_folder(self):
        config_folder = os.path.join(os.path.expanduser('~'), '.moodlefuse')
        if not os.path.exists(config_folder):
            os.makedirs(config_folder)
        os.chmod(config_folder, 0o700)
        return config_folder

    def _create_file_cache(self):
        cache_folder = os.path.join(
            os.path.expanduser('~'),
            '.moodlefuse/cache')
        if not os.path.exists(cache_folder):
            os.makedirs(cache_folder)
        os.chmod(cache_folder, 0o700)
        return cache_folder

    def _create_configuration(self, config_folder):
        args = self._generate_args()
        profile = args.pop('profile')
        config_file_path = config_folder + '/moodlefuse.conf'
        config = self._modify_config_profile(config_file_path, profile)
        self._add_user_to_database(config, profile)
        config_file = open(config_file_path, 'w+')
        config.write(config_file)

    def _create_user_database(self):
        database_file = os.path.join(
            os.path.expanduser('~'),
            '.moodlefuse/moodlefuse.sqlite'
        )

        if not os.path.exists(database_file):
            directory = os.path.join(os.path.dirname(__file__), '../alembic')
            config = AlembicConfig(os.path.join(
                directory,
                'alembic.ini'
            ))
            config.set_main_option('script_location', directory)
            command.upgrade(config, 'head', sql=False, tag=None)

        return 'sqlite:///' + database_file

    def _generate_args(self):
        parser = argparse.ArgumentParser(
            'Command line utility for configuring moodlefuse'
        )

        parser.add_argument(
            '-p',
            '--profile',
            required=False,
            help='The profile to configure, default is initial',
            default='initial'
        )

        args = parser.parse_args()

        return vars(args)

    def _modify_config_profile(self, config_file, profile):
        config = SafeConfigParser()
        config.read(config_file)

        if not config.has_section(profile):
            config.add_section(profile)

        config = self._set_attributes_of_profile(config, profile)

        return config

    def _set_attributes_of_profile(self, config, profile):
        config = self._set_attribute_of_profile(
            config, profile, 'moodle_web_address',
            'Moodle server address',
            'hhtp://www.loop.dcu.ie'
        )

        config = self._set_attribute_of_profile(
            config, profile, 'moodle_index_address',
            'Moodle index address',
            'hhtp://www.loop.dcu.ie/my'
        )

        config = self._set_attribute_of_profile(
            config, profile, 'local_moodle_folder',
            'Local Moodle folder name', 'moodle'
        )

        config = self._set_attribute_of_profile(
            config, profile, 'username',
            'Moodle username', 'username'
        )

        return config

    def _add_user_to_database(self, config, profile):
        attribute_value = self._read_in_config_attribute_or_use_default(
            "Moodle Username", ''
        )

        config.set(profile, 'username', attribute_value)
        password = getpass.getpass('Moodle password:')
        print password

    def _set_attribute_of_profile(self, config, profile, attribute, message, default):
        if config.has_option(profile, attribute):
            default = config.get(profile, attribute)

        attribute_value = self._read_in_config_attribute_or_use_default(
            message,
            default
        )

        config.set(profile, attribute, attribute_value)

        return config

    def _read_in_config_attribute_or_use_default(self, message, default):
        attribute = raw_input(message + ' [' + default + ']: ')
        if attribute == '':
            attribute = default

        return attribute

    def _create_filesystem_folder(self):
        config_folder = os.path.join(os.path.expanduser('~'), 'moodle')
        if not os.path.exists(config_folder):
            os.makedirs(config_folder)
        os.chmod(config_folder, 0o700)
        return config_folder
