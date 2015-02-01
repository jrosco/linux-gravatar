#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gobject
import gtk
import gtk.glade
import appindicator
import gravatar
import settings
import _version as version
import os
import sys


class StartTrayIcon():

    def __init__(self):

        self.gobj = 0
        self.gravatar = gravatar.Gravatar()
        self.icon = '/usr/share/icons/gravatar.png'
        self.setting_menu_icon = '/usr/share/linux-gravatar/settings_menu_icon.png'
        self.refresh_menu_icon = '/usr/share/linux-gravatar/refresh_menu_icon.png'
        self.about_menu_icon = '/usr/share/linux-gravatar/about_menu_icon.png'
        self.close_menu_icon = '/usr/share/linux-gravatar/close_menu_icon.png'
        self.profile_img = '/home/jrosco/.face'

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

    @staticmethod
    def menu_settings(item):

        print 'called menu_settings() %s' % item
        SettingsDialog().run_dialog()

    @staticmethod
    def refresh(item):

        print 'called refresh() %s' % item
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, * sys.argv)

    @staticmethod
    def about(item):

        print 'called about() %s' % item
        AboutDialog().run_dialog()

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

        """ Testing profile pic in menu """
        profile_icon = gtk.Image()
        profile_icon.set_from_file(self.profile_img)
        menu_items = gtk.ImageMenuItem('CURRENT PROFILE')
        #menu_items.connect('activate', self.menu_settings)
        menu_items.set_image(profile_icon)
        menu.append(menu_items)
        menu_items.show()

        sep = gtk.SeparatorMenuItem()
        menu.append(sep)
        sep.show()

        setting_icon = gtk.Image()
        setting_icon.set_from_file(self.setting_menu_icon)
        menu_items = gtk.ImageMenuItem('Settings')
        menu_items.connect('activate', self.menu_settings)
        menu_items.set_image(setting_icon)
        menu.append(menu_items)
        menu_items.show()

        refresh_icon = gtk.Image()
        refresh_icon.set_from_file(self.refresh_menu_icon)
        menu_items = gtk.ImageMenuItem('Refresh')
        menu_items.connect('activate', self.refresh)
        menu_items.set_image(refresh_icon)
        menu.append(menu_items)
        menu_items.show()

        sep = gtk.SeparatorMenuItem()
        menu.append(sep)
        sep.show()

        close_icon = gtk.Image()
        close_icon.set_from_file(self.close_menu_icon)
        menu_items = gtk.ImageMenuItem('Close')
        menu_items.connect('activate', self.close_app)
        menu_items.set_image(close_icon)
        menu.append(menu_items)
        menu_items.show()

        about_icon = gtk.Image()
        about_icon.set_from_file(self.about_menu_icon)
        menu_items = gtk.ImageMenuItem('About')
        menu_items.connect('activate', self.about)
        menu_items.set_image(about_icon)
        menu.append(menu_items)
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
        #self.refresh_gravatar()
        self.refresh(None)

    def close_settings_win(self, widget):

        print 'called close_settings() %s' % widget
        self.settings_dialog.destroy()

    def run_dialog(self):

        print 'called run_dialog()'
        self.settings_dialog.show_all()


class AboutDialog(StartTrayIcon):

    def __init__(self):

        StartTrayIcon.__init__(self)

        """ About GUI Configs"""
        print 'called AboutDialog()'
        #self.builder_file = "../gui/about_win.glade"
        self.builder_file = "/usr/share/linux-gravatar/about_win.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.builder_file)
        self.builder.connect_signals(self)
        self.about_dialog = self.builder.get_object('about_dialog')

    def close_about_win(self, widget):

        print 'called about_dialog_win() %s' % widget
        self.about_dialog.destroy()

    @staticmethod
    def open_homepage():

        print 'called open_project_url()'
        import webbrowser
        webbrowser.open_new_tab(version.__website__)

    def run_dialog(self):

        print 'called run_dialog()'
        self.about_dialog.show_all()
