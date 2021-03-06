from launcher.i18n import gettext
from launcher.settings.plugins_settings_page import PluginsSettingsPage
from system.classes.shellobject import shellObject
from system.classes.windowcache import WindowCache
from system.prefs.components.baseprefswindow import BasePrefsWindow


@shellObject
class Plugin:
    @staticmethod
    def open(**kwargs):
        WindowCache.open(PluginPrefsWindow, **kwargs)


class PluginPrefsWindow(BasePrefsWindow):
    def __init__(self, parent=None):
        super().__init__(parent, title=gettext("Plugin preferences"))
        self.panel = PluginsSettingsPage(self)
        self.layout.add(self.panel, fill=True, expand=True)
