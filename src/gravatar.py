#!/usr/bin/env python

import hashlib
import urllib2
import os
import time
import threading
import settings


class Gravatar(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)
        self.email_addr = None
        self.remote_img = None
        self.local_img = None
        self.check_time = 300
        self.settings = None
        self.location = settings.settings_location()

    def get_url_image(self, email):

        self.email_addr = email

        print 'get_url_image(email)'

        try:
            gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email_addr.lower()).hexdigest()

            response = urllib2.urlopen(gravatar_url)
            self.remote_img = response.read()
        except Exception, e:
            print e

    def save_image(self, image):

        print 'save_image(image)'
        self.get_user_home_image()

        f = open(self.local_img, 'wb')
        f.write(image)
        f.close()

    def get_user_home_image(self):

        print 'get_user_home_image()'
        #self.local_img= '/var/lib/AccountsService/icons/jrosco'
        home_path = os.path.expanduser('~')
        self.local_img = home_path + '/.face'

    def run(self):

        self.settings = settings.GravatarSettings('Settings', self.location)

        md5_image1 = 1
        md5_image2 = 2

        while True:

            print 'compare_images()'

            try:
                self.email_addr = self.settings.read_config('email')
                self.check_time = self.settings.read_config('check')

                self.get_url_image(self.email_addr)
                self.get_user_home_image()

                if os.path.isfile(self.local_img):
                    image_file = open(self.local_img, 'r')
                    md5_image1 = hashlib.md5(image_file.read()).hexdigest()
                    md5_image2 = hashlib.md5(self.remote_img).hexdigest()
                    print md5_image1 + ' : ' + md5_image2
                    image_file.close()
                else:
                    image_file = open(self.local_img, 'a')
                    image_file.write(self.remote_img)
                    image_file.close()

                if str(md5_image1) != str(md5_image2):
                    print 'save image to hdd'
                    self.save_image(self.remote_img)

                time.sleep(float(self.check_time))

            except Exception, e:
                print e