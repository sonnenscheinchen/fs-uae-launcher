from fsui import Image, ImageButton


class IconButton(ImageButton):
    BUTTON_WIDTH = 40

    def __init__(self, parent, name):
        image = Image("launcher:/data/" + name)
        ImageButton.__init__(self, parent, image)
        self.set_min_width(self.BUTTON_WIDTH)

    def set_icon_name(self, name):
        image = Image("launcher:/data/" + name)
        self.set_image(image)
