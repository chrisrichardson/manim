#!/usr/bin/env python

from manimlib import *

class SomeEquations(Scene):

    def construct(self):

        poisson = TexMobject(r"\nabla^2 u = \rho")
        poisson_text = TextMobject("Poisson's Equation")

        VGroup(poisson, poisson_text).arrange(DOWN)
        self.play(Write(poisson), FadeInFrom(poisson_text, DOWN))
        self.wait(5)

        maxwell = VGroup(TexMobject(r"\nabla\times B = \mu_0 (J + \epsilon_0 \dot E)"),
                         TexMobject(r"\nabla\cdot B = 0"),
                         TexMobject(r"\nabla\times E = -\dot B"),
                         TexMobject(r"\nabla\cdot E = {\rho\over\epsilon_0}")
        ).arrange(DOWN)
        maxwell_text = TextMobject("Maxwell's Equations")
        VGroup(maxwell, maxwell_text).arrange(DOWN)

        self.play(ReplacementTransform(poisson, maxwell),
                  ReplacementTransform(poisson_text, maxwell_text))

        self.wait()

        lin_eq = VGroup(TexMobject(r"\epsilon = {1\over 2}(\nabla u + \nabla u^T)"),
                         TexMobject(r"\sigma = C_{ijkl} \epsilon"),
                         TexMobject(r"\nabla \cdot \sigma = f")
        ).arrange(DOWN)
        lin_text = TextMobject("Linear Elasticity")
        VGroup(lin_eq, lin_text).arrange(DOWN)

        self.play(ReplacementTransform(maxwell, lin_eq),
                  ReplacementTransform(maxwell_text, lin_text))

        self.wait(5)

        heat_eq = TexMobject(r"{\partial T \over \partial t} = \nabla\cdot k\nabla T")
        heat_text = TextMobject("Heat Equation")
        VGroup(heat_eq, heat_text).arrange(DOWN)

        self.play(ReplacementTransform(lin_eq, heat_eq),
                  ReplacementTransform(lin_text, heat_text))

        self.wait()

        ns_eq = VGroup(TexMobject(r"\rho\left({\partial u\over\partial t} + u\cdot\nabla u\right) - \mu\nabla^2 u + \nabla p = f"),
                       TexMobject(r"\nabla \cdot u = 0")).arrange(DOWN)
        ns_text = TextMobject("Incompressible Navier-Stokes")
        VGroup(ns_eq, ns_text).arrange(DOWN)

        self.play(ReplacementTransform(heat_eq, ns_eq),
                  ReplacementTransform(heat_text, ns_text))

        self.wait(5)



class Moving(MovingCameraScene):

    def construct(self):

        arc3 = CurvedArrow(np.array([0, 0, 0]),
                           np.array([1, 1, 0]))
        arc4 = CurvedDoubleArrow(np.array([0, 0, 0]),
                                 np.array([-1, -1, 0]))

        img = SVGMobject('fenics_logo_text.svg')
#        img = SVGMobject('m2.svg', stroke_width=0)

        self.play(Write(img))
        return

        self.play(FadeIn(img), Write(arc3), Write(arc4))

        self.camera.frame.generate_target()
        self.camera.frame.target.scale(2.0)
        self.play(MoveToTarget(self.camera.frame))
        self.wait()


class Mesh(VMobject):
    """ Make a 2D triangular mesh """

    def __init__(self, points, cells, **kwargs):
        Mobject.__init__(self, **kwargs)

        for row in cells:
            vertices = [points[j] for j in row]
            tri = self.start_new_path(vertices[2])
            self.add_points_as_corners(vertices)


class SimpleTitle(Scene):

    def construct(self):

        title = TextMobject("Solving matrix equations")
        axb = TexMobject("Ax=b")
        axb.scale(1.4)
        VGroup(title, axb).arrange(DOWN)
        self.play(Write(title), FadeInFrom(axb, UP))
        self.wait()
        self.play(FadeOut(title), LaggedStart(*map(FadeOutAndShiftDown, axb), run_time=3))
        self.wait()


class Help(ThreeDScene):
    CONFIG = {
        "object_center": [0, 0, 0],
        "area_label_center": [0, -1.5, 0],
        "surface_area": 6.0,
        "num_reorientations": 10,
        "camera_config": {
            "light_source_start_point": 10 * OUT,
            "frame_center": [0, 0, 0.5],
        },
        "initial_orientation_config": {
            "phi": 60 * DEGREES,
            "theta": -120 * DEGREES,
        }
    }

    def setup(self):
        self.add_plane()

    def add_plane(self):
        plane = self.plane = Rectangle(
            width=FRAME_WIDTH,
            height=24.2,
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.35,
        )
        plane.set_sheen(0.2, DR)
        grid = NumberPlane(
            color=LIGHT_GREY,
            secondary_color=DARK_GREY,
            y_radius=int(plane.get_height()),
            stroke_width=1,
            secondary_line_ratio=0,
        )
        plane.add(grid)
        plane.add(VectorizedPoint(10 * IN))
        plane.set_shade_in_3d(True, z_index_as_group=True)
        self.add(plane)

    def construct(self):

        import meshio
        mesh = meshio.read('square.msh')

        bm = Mesh(mesh.points, mesh.cells['triangle'], color=RED,
                  fill_color=BLUE, fill_opacity=0.85)
        bm.shift([0,0,0.2])

        verts = [mesh.points[j] for j in mesh.cells['triangle'][10]]
        q = Polygon(*verts, color=GREEN, fill_color=YELLOW, fill_opacity=1.0)
        q.shift([0,0,0.2])
        q.generate_target()
        q.target.scale(1.5)
        q.target.shift([0,0,.5])

        self.play(Write(bm), Write(q))
        self.wait()

        self.move_camera(
            **self.initial_orientation_config,
            run_time=2
        )

        Ax = TexMobject("A_{el}").scale(4)
        Ax.rotate(-PI/2, LEFT)
        Ax.move_to([0,0,3])
        self.play(FadeIn(Ax), MoveToTarget(q))
        self.wait()

        bmat = DecimalMatrix(np.ones((3, 3)))
        bmat.rotate(-PI/2, LEFT)
        bmat.move_to([0,0,3])

        self.play(ReplacementTransform(Ax, bmat))

        self.play(Indicate(bmat))
        self.wait()


class MatrixAlgebra(Scene):

    def construct(self):

        Axb = TexMobject("A", "x", "=", "b").scale(8)

        self.play(FadeIn(Axb))
        self.wait()

        n = 8
        A = np.random.rand(n, n)*20 - 10
        a = DecimalMatrix(A).scale(0.7).move_to([-3,0,0])
        ag = VGroup()
        for ai in a.mob_matrix[3, :]:
            ag.add(ai)

        xa = np.empty((n, 1), dtype=object)
        for i in range(len(xa)):
            xa[i] = TexMobject(r"x_{%d}" % i)
        xb = MobjectMatrix(xa).scale(0.7)
        xb.next_to(a, RIGHT)
        xb.shift([0.1, 0, 0])

        eq = TexMobject("=").scale(1.5).align_to(xb, RIGHT, LEFT).shift([0.2,0,0])

        ba = np.random.rand(n, 1)*20-10
        bb = DecimalMatrix(ba).scale(0.7)
        bb.next_to(eq, RIGHT).shift([0.2,0,0])

        self.play(ReplacementTransform(Axb[0], a, run_time=2),
                  ReplacementTransform(Axb[1], xb, run_time=2),
                  ReplacementTransform(Axb[2], eq, run_time=2),
                  ReplacementTransform(Axb[3], bb, run_time=2))

        self.wait()
        arow = VGroup(*a.mob_matrix[2,:])
        self.play(Indicate(bb.mob_matrix[2, 0]), Indicate(arow), Indicate(xb), Flash(bb.mob_matrix[2, 0]))
        self.wait()

class Simple(Scene):

    def construct(self):

        n = 20

        axes = Axes(x_min = -0.1, x_max = n,
                    y_min = -0.1, y_max = 10)
#                    number_line_config = {"include_tip" : False})
        axes.x_axis.add_numbers(*list(range(0, n + 1)))
        axes.y_axis.add_numbers(*list(range(0, 10)))
#        axes.scale(0.5)
        axes.to_edge(LEFT)

        self.add(axes)

        phi = 0.0
        values = np.array([ 5*(1 + np.cos(TAU*x + phi)) for x in np.linspace(0, 3, n + 1)])
        x = np.linspace(0, n, len(values))
        points = np.array([axes.coords_to_point(*xv) for xv in zip(x, values)])
        graph = DiscreteFunction(points)
        graph.set_color(YELLOW)

        self.set_variables_as_attrs(axes, graph)

        self.play(FadeIn(graph))
        self.wait()

        t = 0
        decimal = Integer(t)
        decimal.add_updater(lambda d: d.set_value(t))
        decimal.to_corner(UP + RIGHT)
        self.add(decimal)
        self.play(Write(decimal))

        graph.generate_target()
        phi = 0.1
        for i in range(20):
            phi = 0.8*i
            t += 1
            values = np.array([ 5*(1 + np.cos(TAU*x + phi)) for x in np.linspace(0, 3, n + 1)])
            points =  np.array([axes.coords_to_point(*xv) for xv in zip(x, values)])

            graph.target.set_values(points)

            #        self.play(Transform(graph, g2, run_time=1))
            self.play(MoveToTarget(graph, run_time=0.4))
#            self.wait()

        return

        obj = DecimalNumber(-3.14159)
        obj.scale(3)
        self.play(FadeIn(obj))
        self.wait()
        self.play(FadeOut(obj))
        self.wait()

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

        title.generate_target().scale(0.5).to_corner(UP + LEFT)
#        title.target.scale(0.5)
#        title.target.to_corner(UP + LEFT)
        self.play(MoveToTarget(title))
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

# camera_config=LOW_QUALITY_CAMERA_CONFIG
# s = Simple(file_writer_config={'write_to_movie':True},
#           camera_config=camera_config)
