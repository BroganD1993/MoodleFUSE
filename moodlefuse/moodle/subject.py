#!/usr/bin/env python
# encoding: utf-8


class Subject(object):

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        print self._observers
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update()