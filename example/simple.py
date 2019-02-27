#!/usr/bin/env python

from manimlib import *

class Simple(Scene):

    def construct(self):
        title = Title("The Title", include_underline=True, match_underline_width_to_text=True)
        self.play(FadeInFrom(title, UP))
        self.wait()

        transform_title = title.copy()
        transform_title.scale(0.5)
        transform_title.to_corner(UP + LEFT)
        self.play(Transform(title, transform_title))
        self.wait()

        v = VGroup()
        tri = Polygon([0,0,0],[0,1,0],[1,0,0], color=GREEN_A)
        d0 = Integer(0)
        d0.scale(0.5)
        d0.move_to([-0.2,-0.2,0])
        d1 = Integer(1)
        d1.move_to([-0.2,1.1,0])
        d1.scale(0.5)
        d2 = Integer(2)
        d2.move_to([1.1,-0.2,0])
        d2.scale(0.5)
        v.add(tri, d0, d1, d2)
        self.play(Write(v))
        v2 = v.copy()
        v2.scale(3.0)
        self.play(Transform(v, v2))
        self.wait()


camera_config=LOW_QUALITY_CAMERA_CONFIG

s = Simple(file_writer_config={'write_to_movie':True},
           camera_config=camera_config)
