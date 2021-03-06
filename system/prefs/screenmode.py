from fsui import Panel
from launcher.i18n import gettext
from system.classes.shellobject import shellObject
from system.classes.windowcache import WindowCache
from system.prefs.components.baseprefswindow import BasePrefsWindow


@shellObject
class ScreenMode:
    @staticmethod
    def open(**kwargs):
        WindowCache.open(ScreenModePrefsWindow, **kwargs)


class ScreenModePrefsWindow(BasePrefsWindow):
    def __init__(self, parent=None):
        super().__init__(parent, title=gettext("Screen mode preferences"))
        self.panel = ScreenModePrefsPanel(self)
        self.layout.add(self.panel, fill=True, expand=True)


class ScreenModePrefsPanel(Panel):
    def __init__(self, parent):
        super().__init__(parent)
        # FIXME
        self.set_min_size((540, 100))
        self.layout.set_padding(20, 0, 20, 20)
