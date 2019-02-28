#!/usr/bin/env python

from manimlib import *




class Simple(Scene):


    def construct(self):
        title = Title("The Title", include_underline=True, match_underline_width_to_text=True)
        self.play(FadeInFrom(title, UP))
        self.wait()

        obj = DecimalNumber(-10)
        obj.scale(3)
        self.play(FadeIn(obj))
        self.wait()

        return

        x = np.linspace(-1,1)
        y = np.sin(8*x)

        q = VMobject()
        p = np.zeros((len(x), 3))
        p[:, 0] = x
        p[:, 1] = y
        q.set_points_as_corners(p)

        self.play(Write(q))
        self.wait()

        img = ImageMobject('7995266112_115d33d6dc_o.jpg')
        self.play(FadeIn(img))
        self.wait()
        self.play(WiggleOutThenIn(img))
        img2 = img.copy()
        img2.to_corner(UP + RIGHT)
        self.play(Transform(img, img2))

        transform_title = title.copy()
        transform_title.scale(0.5)
        transform_title.to_corner(UP + LEFT)
        self.play(Transform(title, transform_title))
        self.wait()

        tri = Polygon([0,0,0],[0,1,0],[1,0,0], color=GREEN_B)
        d0 = Integer(0)
        d0.scale(0.5)
        d0.move_to([-0.2,-0.2,0])
        d1 = Integer(1)
        d1.move_to([-0.2,1.1,0])
        d1.scale(0.5)
        d2 = Integer(2)
        d2.move_to([1.1,-0.2,0])
        d2.scale(0.5)
        v = VGroup()
        v.add(tri, d0, d1, d2)
        self.play(Write(v))
        v2 = v.copy()
        v2.scale(3.0)
        self.play(Transform(v, v2))
        self.wait()

        x = ImageMobjectFromCamera(self.camera)
        x.to_corner(DOWN + RIGHT)
        self.play(FadeIn(x))
        self.wait()

camera_config=LOW_QUALITY_CAMERA_CONFIG

s = Simple(file_writer_config={'write_to_movie':True},
          camera_config=camera_config)
