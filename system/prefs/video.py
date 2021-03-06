from launcher.i18n import gettext
from launcher.settings.video_settings_page import VideoSettingsPage
from system.classes.shellobject import shellObject
from system.classes.windowcache import WindowCache
from system.prefs.components.baseprefswindow import BasePrefsWindow


@shellObject
class Video:
    @staticmethod
    def open(**kwargs):
        WindowCache.open(VideoPrefsWindow, **kwargs)


class VideoPrefsWindow(BasePrefsWindow):
    def __init__(self, parent=None):
        super().__init__(parent, title=gettext("Video preferences"))
        self.panel = VideoSettingsPage(self)
        self.layout.add(self.panel, fill=True, expand=True)
