import fsui
from launcher.i18n import gettext
from launcher.option import Option
from launcher.ui.config.configpanel import ConfigPanel


class ExpansionsPanel(ConfigPanel):
    def __init__(self, parent):
        super().__init__(parent)

        heading_label = fsui.HeadingLabel(self, gettext("Expansions"))
        self.layout.add(heading_label, margin=10)
        self.layout.add_spacer(0)

        # self.add_amiga_option(Option.CPU)
        self.add_amiga_option(Option.ACCELERATOR)
        # self.add_amiga_option(Option.ACCELERATOR_MEMORY)
        self.add_amiga_option(Option.BLIZZARD_SCSI_KIT)
        self.add_amiga_option(Option.GRAPHICS_CARD)
        # self.add_amiga_option(Option.GRAPHICS_MEMORY)
        self.add_amiga_option(Option.SOUND_CARD)
        self.add_amiga_option(Option.NETWORK_CARD)
        # self.add_amiga_option(Option.BSDSOCKET_LIBRARY)

        self.add_amiga_option(Option.FREEZER_CARTRIDGE)
        self.add_amiga_option(Option.DONGLE_TYPE)
