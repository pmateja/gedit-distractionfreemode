from gi.repository import GObject, Gedit, Gtk, Gio
from gettext import gettext as _


FONTSIZE = 12
FONT = ""
WIDTH = 800


class DFMWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "DFMWindowActivatable"
    def_left_margin = 0
    def_right_margin = 0
    def_top_margin = 0
    def_bottom_margin = 0
    show_line_numbers = True
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        action = Gio.SimpleAction(name="dfm_toggle")
        action.connect('activate', self.dfm_toggle)
        self.window.add_action(action)
        self.save()
        self.active = False
        self.window.connect("check-resize", self.dfm, self)

    def do_deactivate(self):
        # Remove any installed menu items
        self.window.remove_action("dfm_toggle")
        self.window.disconnect("dfm", self.dfm, self)
        self._action_group = None

    def do_update_state(self):
        pass

    def save(self):
        view = self.window.get_active_view()
        self.left_margin = view.get_margin_left()
        self.right_margin = view.get_margin_right()
        self.top_margin = view.get_margin_top()
        self.bottom_margin = view.get_margin_bottom()
        self.show_line_numbers = view.get_show_line_numbers()
        
    def dfm_toggle(self, container, widget):
        self.active = not self.active
        self.dfm()
    
    def dfm(self, container, widget):
        view = self.window.get_active_view()
        window = self.window
        if not self.active:
            self.save()
            w, h = self.window.get_size()
            margin = (w - WIDTH) / 2
            view.set_margin_left(margin)
            view.set_margin_right(margin)
            view.set_margin_top(20)
            view.set_margin_bottom(20)
            view.set_show_line_numbers(False)
            window.fullscreen()
            #self.active = True
        else:
            #view.set_left_margin(0)
            #view.set_right_margin(0)
            view.set_margin_left(self.left_margin)
            view.set_margin_right(self.right_margin)
            view.set_margin_top(self.top_margin)
            view.set_margin_bottom(self.bottom_margin)
            view.set_show_line_numbers(self.show_line_numbers)
            window.unfullscreen()
            #self.active = False


class DFMViewActivatable(GObject.Object, Gedit.ViewActivatable):
    __gtype_name__ = "DFMViewActivatable"

    view = GObject.property(type=Gedit.View)

    def __init__(self):
        GObject.Object.__init__(self)


    def do_activate(self):
        print("Plugin created for", self.view)
        print("XXXXXXXXX")
        print(self.view.get_margin_top())                

    def do_deactivate(self):
        print("Plugin stopped for", self.view)

    def do_update_state(self):
        # Called whenever the view has been updated
        print("Plugin update for", self.view)

class FFMAppActivatable(GObject.Object, Gedit.AppActivatable):

    app = GObject.Property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.app.add_accelerator("<Alt>F11", "win.dfm_toggle", None)
        self.menu_ext = self.extend_menu("tools-section")
        item = Gio.MenuItem.new(_("Distraction Free"), "win.dfm_toggle")
        self.menu_ext.append_menu_item(item) 

    def do_deactivate(self):
        self.app.remove_accelerator("win.dfm_toggle", None)
        self.menu_ext = None
