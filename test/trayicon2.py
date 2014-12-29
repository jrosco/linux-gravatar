#!/usr/bin/env python

import gobject
import gtk
import appindicator


def menu_settings(item):

    print 'Settings %s' % item
    filename = '../gui/settings_win.glade'
    builder = gtk.Builder()
    builder.add_from_file(filename)


def close_app(item):

    print 'Close %s' % item
    gtk.main_quit()

if __name__ == "__main__":
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
    menu_items.connect('activate', menu_settings)
    menu_items.show()

    menu_items = gtk.MenuItem('Close')
    menu.append(menu_items)
    menu_items.connect('activate', close_app)
    menu_items.show()

    ind.set_menu(menu)

    gtk.main()