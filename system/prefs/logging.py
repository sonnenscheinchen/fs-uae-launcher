from fsgamesys.options.option import Option
from fsui import MultiLineLabel
from launcher.i18n import gettext
from system.classes.shellobject import shellObject
from system.classes.windowcache import WindowCache
from system.prefs.components.baseprefspanel import BasePrefsPanel
from system.prefs.components.baseprefswindow import BasePrefsWindow
from system.prefs.components.notworking import PrefsNotWorkingWarningPanel


@shellObject
class Logging:
    @staticmethod
    def open(**kwargs):
        WindowCache.open(LoggingPrefsWindow, **kwargs)


class LoggingPrefsWindow(BasePrefsWindow):
    def __init__(self, parent=None):
        super().__init__(parent, title=gettext("Logging preferences"))
        self.panel = LoggingPrefsPanel(self)
        self.layout.add(self.panel, fill=True, expand=True)


class LoggingPrefsPanel(BasePrefsPanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout.set_padding(20, 0, 20, 20)

        self.layout.add_spacer(20)
        PrefsNotWorkingWarningPanel(parent=self)

        label = MultiLineLabel(
            self,
            gettext(
                "The following options may affect performance, "
                "so only enable them when needed for testing or "
                "debugging purposes."
            ),
            440,
        )
        self.layout.add(label, fill=True, margin_top=20)

        self.add_option(Option.LOG_AUTOSCALE)
        self.add_option(Option.LOG_INPUT)
