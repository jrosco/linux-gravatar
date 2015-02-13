#!/usr/bin/env python

""" Supports python2 and python3"""
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

import hashlib
import os
import dbus
import pwd
import time
import threading
from . import settings
import logging


class Gravatar(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)
        logging.basicConfig(level=logging.INFO)
        self.email_addr = None
        self.remote_img = None
        self.local_img = None
        self.check_time = 60.0
        self.stop_thread = False
        self.settings = None
        self.location = settings.settings_location()
        self.settings = settings.GravatarSettings('Settings', self.location)

    def get_url_image(self, email):

        self.email_addr = email

        logging.debug('get_url_image(email)')

        try:
            email_m5d = hashlib.md5(self.email_addr.lower().encode()).hexdigest()
            logging.debug('connecting to gravatar site')
            gravatar_url = "http://www.gravatar.com/avatar/" + email_m5d
            response = urlopen(gravatar_url)
            self.remote_img = response.read()
            logging.debug('got remote img from gravatar site')

        except RuntimeError as e:
            logging.error('URL Error: %s' % e)

    def save_image(self, image):

        logging.debug('save_image(image)')
        self.get_user_home_image()

        try:
            f = open(str(self.local_img), 'wb')
            f.write(image)
            f.close()

        except IOError as e:
            logging.error('IO Error: %s' % e)

    def set_dbus_icon(self):

        logging.debug('set_dbus_icon()')

        user_id = pwd.getpwuid(os.getuid()).pw_uid
        icon_file = self.local_img

        bus_name = 'org.freedesktop.Accounts'
        object_path = '/org/freedesktop/Accounts/User'
        interface_name = 'org.freedesktop.Accounts.User'

        try:
            session_bus = dbus.SystemBus()

            user_name = session_bus.get_object(bus_name, object_path + str(user_id))
            properties_manager = dbus.Interface(user_name, dbus_interface='org.freedesktop.DBus.Properties')
            properties_manager.SetIconFile(icon_file, dbus_interface=interface_name)

            self.notify(summary='linux-gravatar', body='<u>Added a new gravatar</u>')

        except dbus.DBusException as e:
            logging.error('DBUS Error: %s ' % e)

    #TODO: Maybe move this to trayicon.py
    def notify(self, summary, body='', app_name='', app_icon='', timeout=-1, actions=[], hints=[], replaces_id=0):

        if self.settings.read_config_bool('notifications') is True:
            bus_name = 'org.freedesktop.Notifications'
            object_path = '/org/freedesktop/Notifications'
            interface_name = bus_name

            try:
                session_bus = dbus.SessionBus()
                obj = session_bus.get_object(bus_name, object_path)
                interface = dbus.Interface(obj, interface_name)
                interface.Notify(app_name, replaces_id, app_icon, summary, body, actions, hints, timeout)

            except dbus.DBusException as e:
                logging.error('DBUS Error: %s' % e)

    def get_user_home_image(self):

        logging.debug('get_user_home_image()')
        home_path = os.path.expanduser('~')
        self.local_img = home_path + '/.face'
        return self.local_img

    def main(self):

        md5_image1 = 1
        md5_image2 = 2

        logging.debug('called do_gravatar()')
        try:
                self.email_addr = self.settings.read_config('email')

                self.get_url_image(self.email_addr)
                self.get_user_home_image()

                if os.path.isfile(self.local_img):
                    image_file = open(str(self.local_img), 'rb')
                    md5_image1 = hashlib.md5(image_file.read()).hexdigest()
                    md5_image2 = hashlib.md5(self.remote_img).hexdigest()
                    logging.debug(md5_image1 + ' : ' + md5_image2)
                    image_file.close()
                else:
                    try:
                        image_file = open(str(self.local_img), 'a')
                        image_file.write(self.remote_img)
                        image_file.close()
                    except IOError as e:
                        logging.error('IOERROR: %s' % e)

                if str(md5_image1) != str(md5_image2):
                    logging.debug('save image to hdd')
                    self.save_image(self.remote_img)
                    self.set_dbus_icon()

                return True

        except RuntimeError as e:
            logging.error('Main Error: %s' % e)
            return False

    def run(self):

        while True:

            logging.debug('compare_images(%s)' % threading.currentThread())

            self.check_time = self.settings.read_config('check')

            # print threading.enumerate()[0]
            #
            # if threading.activeCount() > 2:
            #     if threading.enumerate()[0]:
            #
            #         break
            #     #self.stop_thread = True

            self.main()
            time.sleep(float(self.check_time) * 60)
            #time.sleep(float(self.check_time))