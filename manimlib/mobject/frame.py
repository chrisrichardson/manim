from manimlib.constants import FRAME_HEIGHT, BLACK
from manimlib.mobject.geometry import Rectangle
from manimlib.utils.config_ops import digest_config


class ScreenRectangle(Rectangle):

    def __init__(self, aspect_ratio=16/9, height=4, **kwargs):
        self.aspect_ratio = aspect_ratio
        self.height = 4
        Rectangle.__init__(self, **kwargs)
        self.set_width(
            self.aspect_ratio * self.get_height(),
            stretch=True
        )


class FullScreenRectangle(ScreenRectangle):
    CONFIG = {
        "height": FRAME_HEIGHT,
    }


class FullScreenFadeRectangle(FullScreenRectangle):
    CONFIG = {
        "stroke_width": 0,
        "fill_color": BLACK,
        "fill_opacity": 0.7,
    }


class PictureInPictureFrame(Rectangle):
    CONFIG = {
        "height": 3,
        "aspect_ratio": 16.0 / 9.0
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        Rectangle.__init__(
            self,
            width=self.aspect_ratio * self.height,
            height=self.height,
            **kwargs
        )
