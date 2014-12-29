#!/usr/bin/env python

import threading
import gravatar


class MyThread (threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)

    def run(self):

        print "Starting " + self.name
        gravatar.Gravatar().start()
        print "Exiting " + self.name


f = MyThread()
f.start()
