from gi.repository import GObject, Gedit, Gtk, Gio, GLib
from gettext import gettext as _


WIDTH = 800


class DFMWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "DFMWindowActivatable"
    left_margin = 0
    right_margin = 0
    top_margin = 0
    bottom_margin = 20
    show_line_numbers = True
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.active = False
        action = Gio.SimpleAction.new_stateful("distractionfree", None, GLib.Variant.new_boolean(False))
        action.connect('activate', self.dfm_toggle)
        self.window.add_action(action)
        
    def do_deactivate(self):
        self.window.remove_action("distractionfree")
        self._action_group = None

    def do_update_state(self):
        pass

    def save(self):
        window = self.window
        view = window.get_active_view()
        if view is None:
            pass
        else:
            if not self.active:
                view = self.window.get_active_view()
                self.left_margin = view.get_left_margin()
                self.right_margin = view.get_right_margin()
                self.top_margin = view.get_margin_top()
                self.bottom_margin = view.get_margin_bottom()
                self.show_line_numbers = view.get_show_line_numbers()

    def dfm_toggle(self, action, parameter):
        window = self.window
        view = window.get_active_view()
        #self.save()
        self.active = not self.active
        action.set_state(GLib.Variant.new_boolean(self.active))
        self.dfm()
        if self.active:
            self.coid = self.window.connect("check-resize", self.dfm, self)
        else:
            self.window.disconnect(self.coid)

    def dfm(self, container=None, widget=None):
        window = self.window
        view = window.get_active_view()
        if view is None:
            pass
        else:
            if self.active:
                self.save()
                w, h = self.window.get_size()
                margin = (w - WIDTH) / 2
                view.set_left_margin(margin)
                view.set_right_margin(margin)
                view.set_margin_top(20)
                view.set_margin_bottom(20)
                view.set_show_line_numbers(False)
                window.fullscreen()
            else:
                view.set_left_margin(self.left_margin)
                view.set_right_margin(self.right_margin)
                view.set_margin_top(self.top_margin)
                view.set_margin_bottom(self.bottom_margin)
                view.set_show_line_numbers(self.show_line_numbers)
                window.unfullscreen()


class DFMAppActivatable(GObject.Object, Gedit.AppActivatable):

    app = GObject.Property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.menu_ext = self.extend_menu("tools-section")
        item = Gio.MenuItem.new(_("Distraction Free"), "win.distractionfree")
        
        self.menu_ext.append_menu_item(item)
        self.app.add_accelerator("<Alt>F11", "win.distractionfree", None)

    def do_deactivate(self):
        self.app.remove_accelerator("win.distractionfree")
        self.menu_ext = None
