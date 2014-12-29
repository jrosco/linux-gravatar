#!/usr/bin/env python

import gobject
import gtk
import appindicator
import src.gravatar


class StartTrayIcon():

    def __init__(self):

        self.gobj = 0
        self.gravatar = src.gravatar.Gravatar()
        self.settings_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.settings_box = gtk.HBox(False, 0)
        self.email_value = gtk.Entry()

    def gravatar_object(self):

        self.gobj = gobject.timeout_add(0, self.start_gravatar)

    def start_gravatar(self):

        self.gravatar.setDaemon(True)
        self.gravatar.start()

    def menu_settings(self, item):

        print 'Settings %s' % item
        self.settings_window.set_title("Settings")
        self.settings_window.set_size_request(400, 200)
        self.settings_window.add(self.settings_box)
        self.settings_box.pack_start(self.email_value, True, True, 0)
        self.email_value.show()
        self.settings_window.show()

    def close_app(self, item):

        print 'Close %s' % item
        gtk.main_quit()

    def run(self):

        gobject.threads_init()

        ind = appindicator.Indicator("linux-gravatar",
                                     "indicator-messages",
                                     appindicator.CATEGORY_APPLICATION_STATUS)
        ind.set_status(appindicator.STATUS_ACTIVE)
        icon = '../media/gravatar.png'
        ind.set_icon(icon)

        # create a menu
        menu = gtk.Menu()

        menu_items = gtk.MenuItem('Settings')
        menu.append(menu_items)
        menu_items.connect('activate', self.menu_settings)
        menu_items.show()

        menu_items = gtk.MenuItem('Close')
        menu.append(menu_items)
        menu_items.connect('activate', self.close_app)
        menu_items.show()

        ind.set_menu(menu)

        self.gravatar_object()

        gtk.main()