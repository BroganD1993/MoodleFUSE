#!/usr/bin/env python
# encoding: utf-8

from moodlefuse.moodle.moodle_watcher import MoodleWatcher


def main():
    watcher = MoodleWatcher()
    watcher.start()


if __name__ == "__main__":
    main()
