import gtk

class MainWindow():

    def __init__(self):
        self.window = gtk.Window()
        self.box = gtk.EventBox ()
        self.window.add (self.box)
        self.box.add (gtk.Label ('some text'))
        self.window.set_can_focus(True)
        self.window.show_all()

        self.box.connect('focus-out-event', self.foo)

    def foo(self, widget, event):
        print 'foo'
        if not event:
            print 'outside'
        else:
            print 'inside'

if __name__ == "__main__":
    main = MainWindow()
    gtk.main()
