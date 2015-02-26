#!/usr/bin/env python
# encoding: utf-8

import os
import errno

from moodlefuse.filesystem import Filesystem
from moodlefuse.core import setup, config


class MoodleFuse(object):

    def __init__(self):
        setup()
        self._create_filesystem_root()
        Filesystem(config['LOCAL_MOODLE_FOLDER'])

    def _create_filesystem_root(self):
        moodle_fs_path = config['LOCAL_MOODLE_FOLDER']
        try:
            os.makedirs(moodle_fs_path)
        except OSError, e:
            if e.errno is not errno.EEXIST:
                raise e
