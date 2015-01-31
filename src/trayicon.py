#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gobject
import gtk
import gtk.glade
import appindicator
import gravatar
import settings


class StartTrayIcon():

    def __init__(self):

        self.gobj = 0
        self.gravatar = gravatar.Gravatar()
        self.icon = '/usr/share/icons/gravatar.png'

    def gravatar_object(self):

        self.gobj = gobject.timeout_add(0, self.start_gravatar)

    def start_gravatar(self):

        print 'called start_gravatar(%s)' % self.gravatar
        self.gravatar.setDaemon(True)
        self.gravatar.start()

    def refresh_gravatar(self):

        print 'called refresh_gravatar(%s)' % self.gravatar

        if not self.gravatar.is_alive():
            print 'Thread Refresher'
            self.start_gravatar()

    def menu_settings(self, item):

        print 'called menu_settings() %s' % item
        SettingsDialog().run_dialog()

    @staticmethod
    def close_app(item):

        print 'called close_app() %s' % item
        gtk.main_quit()

    def run(self):

        gobject.threads_init()

        ind = appindicator.Indicator("linux-gravatar",
                                     "indicator-messages",
                                     appindicator.CATEGORY_APPLICATION_STATUS)
        ind.set_status(appindicator.STATUS_ACTIVE)
        ind.set_icon(self.icon)

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


class SettingsDialog(StartTrayIcon):

    def __init__(self):

        StartTrayIcon.__init__(self)

        """ Settings GUI Configs"""
        print 'called SettingsDialog()'
        #self.builder_file = "../gui/settings_win.glade"
        self.builder_file = "/usr/share/linux-gravatar/settings_win.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.builder_file)
        self.builder.connect_signals(self)
        self.settings_dialog = self.builder.get_object('settings')
        self.email_txt = self.builder.get_object('email_txt')
        self.check_int = self.builder.get_object('check_int')

        self.config_values = settings.GravatarSettings('Settings', settings.settings_location())
        self.email_value = self.config_values.read_config('email')
        self.email_txt.set_text(self.email_value)
        self.check_value = float(self.config_values.read_config('check'))
        self.check_int.set_value(self.check_value)

    def apply_settings(self, widget):

        print 'called apply_settings()'
        self.config_values.save_to_config('email', self.email_txt.get_text())
        self.config_values.save_to_config('check', self.check_int.get_value())
        self.settings_dialog.destroy()
        #print self.gravatar
        self.refresh_gravatar()

    def close_settings_win(self, widget):

        print 'called close_settings() %s' % widget
        self.settings_dialog.destroy()

    def run_dialog(self):

        print 'called run_dialog()'
        self.settings_dialog.show_all()
