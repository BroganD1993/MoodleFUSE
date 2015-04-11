#!/usr/bin/env python
# encoding: utf-8

import os

from moodlefuse.helpers import get_cache_path_based_on_location
from moodlefuse.filesystem.files.file import File


class CacheFile(File):

    def __init__(self, cache_path):
        super(CacheFile, self).__init__()
        self.path = cache_path
        st = os.lstat(cache_path)

        self.attrs = dict(
            (key, getattr(st, key)) for key in (
                'st_atime',
                'st_ctime',
                'st_gid',
                'st_mode',
                'st_mtime',
                'st_nlink',
                'st_size',
                'st_uid'
            )
        )

    @staticmethod
    def create_file(location):
        cache_path = get_cache_path_based_on_location(location)
        with open(cache_path, 'w'):
            return cache_path

    @staticmethod
    def write_to_file(location):
        cache_path = get_cache_path_based_on_location(location)
