from fsui import Panel
from launcher.i18n import gettext
from system.classes.shellobject import shellObject
from system.classes.windowcache import WindowCache
from system.prefs.components.baseprefswindow import BasePrefsWindow


@shellObject
class Overscan:
    @staticmethod
    def open(**kwargs):
        WindowCache.open(OverscanPrefsWindow, **kwargs)


class OverscanPrefsWindow(BasePrefsWindow):
    def __init__(self, parent=None):
        super().__init__(parent, title=gettext("Overscan preferences"))
        self.panel = OverscanPrefsPanel(self)
        self.layout.add(self.panel, fill=True, expand=True)


class OverscanPrefsPanel(Panel):
    def __init__(self, parent):
        super().__init__(parent)
        # FIXME
        self.set_min_size((540, 100))
        self.layout.set_padding(20, 0, 20, 20)
