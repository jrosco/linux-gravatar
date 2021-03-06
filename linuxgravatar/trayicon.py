#!/usr/bin/env python

""" Supports python2 and python3"""
try:
    import pygtk
    pygtk.require('2.0')
    import gobject
    import gtk
    import gtk.glade
except ImportError:
    import gi
    #from gi import pygtkcompat
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk as gtk
    from gi.repository import GObject as gobject

from . import gravatar
from . import settings
from . import _version as version
import logging
import os
import sys


class StartTrayIcon():

    def __init__(self):

        self.gobj = 0
        self.gravatar = gravatar.Gravatar()
        logging.basicConfig(level=logging.INFO)
        self.icon = '/usr/share/icons/gravatar.png'
        self.setting_menu_icon = '/usr/share/linux-gravatar/settings_menu_icon.png'
        self.view_profile_menu_icon = '/usr/share/linux-gravatar/profile_menu_icon.png'
        self.refresh_menu_icon = '/usr/share/linux-gravatar/refresh_menu_icon.png'
        self.about_menu_icon = '/usr/share/linux-gravatar/about_menu_icon.png'
        self.close_menu_icon = '/usr/share/linux-gravatar/close_menu_icon.png'
        self.profile_img = self.gravatar.get_user_home_image()
        self.config_values = settings.GravatarSettings('Settings', settings.settings_location())
        self.notify_enabled = self.config_values.read_config_bool('notifications')

    def gravatar_object(self):

        self.gobj = gobject.timeout_add(0, self.start_gravatar)

    def start_gravatar(self):

        logging.debug('called start_gravatar(%s)' % self.gravatar)
        self.gravatar.setDaemon(True)
        self.gravatar.start()

    def notify_action(self, widget, data=None):

        logging.debug('called notify_action(%s)' % widget.get_active())
        notify_enabled = widget.get_active()
        self.config_values.save_to_config('notifications', str(notify_enabled))

    @staticmethod
    def menu_settings(item):

        logging.debug('called menu_settings() %s' % item)
        SettingsDialog().run_dialog()

    @staticmethod
    def menu_profile_dialog(item):

        logging.debug('called menu_profile_dialog() %s' % item)
        ProfileDialog().run_dialog()

    @staticmethod
    def refresh(item):

        logging.debug('called refresh() %s' % item)
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        if gravatar.Gravatar().main():
            python = sys.executable
            os.execl(python, python, * sys.argv)

    @staticmethod
    def menu_open_profile(item):

        logging.debug('called menu_open_profile(%s)' % item)

        try:
            import webbrowser
            config_values = settings.GravatarSettings('Settings', settings.settings_location())
            user_value = config_values.read_config('username')

            if not user_value:
                gravatar.Gravatar().notify(summary='linux-gravatar', body='<u> WARNING username not set.</u>')
                webbrowser.open_new_tab('http://gravatar.com/')
            else:
                webbrowser.open_new_tab('http://gravatar.com/profile/' + user_value)

        except RuntimeError as e:
            logging.error('open profile error: %e' % e)

    @staticmethod
    def about(item):

        logging.debug('called about() %s' % item)
        AboutDialog().run_dialog()

    @staticmethod
    def close_app(item):

        logging.debug('called close_app() %s' % item)
        gtk.main_quit()

    def run(self):

        #gtk.rc_parse('../gui/gtkrc')

        gobject.threads_init()

        try:
            """ Python 2 Appindicator """
            import appindicator
            ind = appindicator.Indicator("linux-gravatar",
                                         self.icon,
                                         appindicator.CATEGORY_APPLICATION_STATUS)
            ind.set_status(appindicator.STATUS_ACTIVE)
        except ImportError:
            gi.require_version('AppIndicator3', '0.1')
            from gi.repository import AppIndicator3 as appindicator
            """ Python 3 Appindicator """
            ind = appindicator.Indicator.new_with_path(("linux-gravatar"),
                                                        self.icon,
                                                        appindicator.IndicatorCategory.APPLICATION_STATUS,
                                                        '')
            ind.set_status(appindicator.IndicatorStatus.ACTIVE)
            ind.set_attention_icon(self.icon)

        # create a menu
        menu = gtk.Menu()

        """ Testing profile pic in menu """
        profile_icon = gtk.Image()
        profile_icon.set_from_file(self.profile_img)
        menu_items = gtk.ImageMenuItem('CURRENT PROFILE')
        menu_items.connect('activate', self.menu_profile_dialog)
        menu_items.set_image(profile_icon)
        menu.append(menu_items)

        """ Set Menu Color"""
        #style = menu_items.get_style().copy()
        #style.bg[gtk.STATE_NORMAL] = menu_items.get_colormap().alloc_color(0x0000, 0x0000, 0x0000)
        #menu_items.set_style(style)

        menu_items.show()

        sep = gtk.SeparatorMenuItem()
        menu.append(sep)
        sep.show()

        check = gtk.CheckMenuItem("Enable Notifications")
        check.set_active(self.notify_enabled)
        check.connect('toggled', self.notify_action, '')
#        check.connect_object('activate', self.about_menu_icon) #TODO:Change this!!
        menu.append(check)
        check.show()

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


        view_profile_icon = gtk.Image()
        view_profile_icon.set_from_file(self.view_profile_menu_icon)
        menu_items = gtk.ImageMenuItem('View Profile')
        menu_items.connect('activate', self.menu_open_profile)
        menu_items.set_image(view_profile_icon)
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
        logging.debug('called SettingsDialog()')
        self.builder_file = "/usr/share/linux-gravatar/settings_win.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.builder_file)
        self.builder.connect_signals(self)
        self.settings_dialog = self.builder.get_object('settings')

        self.user_txt = self.builder.get_object('user_txt')
        self.email_txt = self.builder.get_object('email_txt')
        self.check_int = self.builder.get_object('check_int')

        self.user_value = self.config_values.read_config('username')
        self.user_txt.set_text(self.user_value)
        self.email_value = self.config_values.read_config('email')
        self.email_txt.set_text(self.email_value)
        self.check_value = float(self.config_values.read_config('check'))
        self.check_int.set_value(self.check_value)

    def apply_settings(self, widget):

        logging.debug('called apply_settings()')
        self.config_values.save_to_config('username', self.user_txt.get_text())
        self.config_values.save_to_config('email', self.email_txt.get_text())
        self.config_values.save_to_config('check', str(self.check_int.get_value()))
        self.settings_dialog.destroy()
        #self.refresh_gravatar()
        self.refresh(None)

    def close_settings_win(self, widget):

        logging.debug('called close_settings() %s' % widget)
        self.settings_dialog.destroy()

    def run_dialog(self):

        logging.debug('called run_dialog()')
        self.settings_dialog.show_all()


class AboutDialog(StartTrayIcon):

    def __init__(self):

        StartTrayIcon.__init__(self)

        """ About GUI Configs"""
        logging.debug('called AboutDialog()')
        self.builder_file = "/usr/share/linux-gravatar/about_win.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.builder_file)
        self.builder.connect_signals(self)
        self.about_dialog = self.builder.get_object('about_dialog')

    def close_about_win(self, widget):

        logging.debug('called about_dialog_win() %s' % widget)
        self.about_dialog.destroy()

    def open_homepage(self, widget):

        logging.debug('called open_project_url(%s)' % widget)
        try:
            import webbrowser
            webbrowser.open_new_tab(version.__website__)
        except RuntimeError as e:
            logging.error('open project site error: %e' % e)
        self.about_dialog.destroy()

    def open_my_profile(self, widget):

        logging.debug('called open_my_profile(%s)' % widget)
        try:
            import webbrowser
            webbrowser.open_new_tab(version.__profile__)
        except RuntimeError as e:
            logging.error('open project site error: %e' % e)
        self.about_dialog.destroy()

    def run_dialog(self):

        logging.debug('called run_dialog()')
        self.about_dialog.show_all()


class ProfileDialog(StartTrayIcon):

    def __init__(self):

        StartTrayIcon.__init__(self)

        """ Profile GUI Configs"""
        logging.debug('called ProfileDialog()')
        self.builder_file = "/usr/share/linux-gravatar/profile_win.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.builder_file)
        self.builder.connect_signals(self)
        self.profile_dialog = self.builder.get_object('profile_dialog')
        self.username_txt = self.builder.get_object('username_txt')
        self.email_txt = self.builder.get_object('email_txt')
        self.profile_img = self.builder.get_object('profile_img')

        self.config_values = settings.GravatarSettings('Settings', settings.settings_location())
        settings_username = self.config_values.read_config('username')
        settings_email = self.config_values.read_config('email')

        if settings_username:
            self.username_txt.set_text(settings_username)

        if settings_email:
            self.email_txt.set_text(settings_email)

        self.profile_img.set_from_file(self.gravatar.get_user_home_image())

    def close_profile_win(self, widget):

        logging.debug('called close_profile_win() %s' % widget)
        self.profile_dialog.destroy()

    def open_settings(self, widget):

        logging.debug('called open_settings(%s)' % widget)
        SettingsDialog().run_dialog()

        self.profile_dialog.destroy()

    def open_my_profile(self, widget):

        logging.debug('called open_my_profile(%s)' % widget)
        self.menu_open_profile(widget)
        self.profile_dialog.destroy()

    def run_dialog(self):

        logging.debug('called run_dialog()')
        self.profile_dialog.show_all()
