#!/usr/bin/env python

import gtk
import gobject
import gtk.glade
import gravatar


class StartTrayIcon():

    def __init__(self):

        self.gobj = 0
        self.gravatar = gravatar.Gravatar()
        self.settings_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.settings_box = gtk.HBox(False, 0)
        self.email_value = gtk.Entry()

    def gravatar_object(self):

        self.gobj = gobject.timeout_add(0, self.start_gravatar)

    def start_gravatar(self):

        self.gravatar.setDaemon(True)
        self.gravatar.start()

    @staticmethod
    def message(data=None):
        """ Function to display messages to the user."""

        msg = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                                gtk.MESSAGE_INFO, gtk.BUTTONS_OK, data)
        msg.run()
        msg.destroy()

    def settings(self):

        filename = '../gui/settings_win.glade'
        builder = gtk.Builder()
        builder.add_from_file(filename)
        #builder.connect_signals(self)
        # self.settings_window.set_title("Settings")
        # self.settings_window.set_size_request(400, 200)
        # self.settings_window.add(self.settings_box)
        # self.settings_box.pack_start(self.email_value, True, True, 0)
        # self.email_value.show()
        # self.settings_window.show()

    def open_app(self, data=None):

        #self.message(data)
        self.settings()

    def close_app(self, data=None):

        gtk.main_quit()

    def make_menu(self, event_button, event_time, data=None):

        menu = gtk.Menu()
        open_item = gtk.MenuItem("Settings")
        close_item = gtk.MenuItem("Close")

        # Append the menu items
        menu.append(open_item)
        menu.append(close_item)
        # add callbacks
        open_item.connect_object("activate", self.open_app, "Settings")
        close_item.connect_object("activate", self.close_app, "Close App")
        # Show the menu items
        open_item.show()
        close_item.show()

        #Popup the menu
        menu.popup(None, None, None, event_button, event_time)

    def on_right_click(self, data, event_button, event_time):

        self.make_menu(event_button, event_time)

    def run(self):

        gobject.threads_init()
        icon = gtk.status_icon_new_from_file('../media/gravatar.png')
        icon.connect('popup-menu', self.on_right_click)
        self.gravatar_object()
        gtk.main()