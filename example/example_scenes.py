#!/usr/bin/env python

from manimlib import *

# To watch one of these scenes, run the following:
# python -m manimlib example_scenes.py SquareToCircle -pl
#
# Use the flat -l for a faster rendering at a lower
# quality.
# Use -s to skip to the end and just save the final frame
# Use the -p to have the animation (or image, if -s was
# used) pop up once done.
# Use -n <number> to skip ahead to the n'th animation of a scene.

def Kmat(p, geometry):
    ''' Calculate K from the points '''
    # p contains the indices of the three points
    # making up the triangle
    assert(len(p) == 3)
    x0, y0 = geometry[p[0]]
    x1, y1 = geometry[p[1]]
    x2, y2 = geometry[p[2]]

    # Element area Ae
    Ae = 0.5*abs((x0 - x1)*(y2 - y1) - (y0 - y1)*(x2 - x1))

    # 'B' Matrix - representing the 'gradient' operator
    B = np.array([[y1 - y2, y2 - y0, y0 - y1],
                  [x2 - x1, x0 - x2, x1 - x0]])/(2*Ae)

    K = Ae*np.matmul(B.transpose(), B)
    return K

class FiniteElement(Scene):

    def construct(self):

        if True:
            title = TextMobject("The Finite Element Method")
            self.play(Write(title))
            self.wait()

            transform_title = TextMobject("The Finite Element Method")
            transform_title.to_corner(UP + LEFT)
            transform_title.scale(0.7)

            poisson_strong = TexMobject(r"\nabla^2 u = \rho")
            poisson_strong.scale(1.5)

            self.play(
                Transform(title, transform_title),
                LaggedStart(FadeInFrom(poisson_strong, UP))
            )
            self.wait()

            poisson_weak = TexMobject(r"\int \nabla u \cdot \nabla v\ d\Omega = \int \rho\ v d\Omega")
            print(UP, LEFT, RIGHT, OUT, IN, ORIGIN, DOWN)
            poisson_weak.to_corner(2*UP + LEFT)
            self.play(
                Transform(poisson_strong, poisson_weak)
            )
            self.wait()

            mesh = VGroup()
            n = 5
            dx = 5.0
            dy = 4.0
            for i in range(n):
                for j in range(n):
                    x0 = (i/n - 0.5)*dx
                    y0 = (j/n - 0.5)*dy
                    x = np.array([[x0, y0, 0], [x0+dx/n, y0, 0],
                                  [x0, y0+dy/n, 0], [x0+dx/n, y0+dy/n, 0]])
                    p = Polygon(x[0], x[1], x[2])
                    mesh.add(p)
                    p = Polygon(x[1], x[2], x[3])
                    mesh.add(p)

            self.play(Write(mesh))
            self.wait()
            self.play(FadeOut(mesh))

        x0 = -0.3
        dx = 1.0
        y0 = 0.7
        dy = -0.66
        A = VGroup()
        transform_A = VGroup()
        array = TexMobject(r"""K_{\rm el} = \left(\begin{matrix}  \qquad & \qquad \\
                                                     \\ \\  \end{matrix}\right)""")
        for i in range(3):
            for j in range(3):
                aij = TexMobject(r"A_{%d%d}"%(i,j))
                aij.move_to(np.array([x0+j*dx, y0+i*dy, 0]))
                A.add(aij)
                vij = DecimalNumber(
                    float(i-j),
                    num_decimal_places=2)
                vij.scale(0.5)
                vij.move_to(np.array([x0+j*dx, y0+i*dy, 0]))
                transform_A.add(vij)
        A.add(array)
        transform_A.add(array.copy())

        self.play(Write(A))
        self.wait()

        transform_A.move_to(UP*3 + RIGHT*4)
        transform_A.scale(0.75)

        self.play(Transform(A, transform_A))
        self.wait()


class OpeningManimExample(Scene):
    def construct(self):
        title = TextMobject("This is some \\LaTeX")
        basel = TexMobject(
            "\\sum_{n=1}^\\infty "
            "\\frac{1}{n^2} = \\frac{\\pi^2}{6}"
        )
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeInFrom(basel, UP),
        )
        self.wait()

        transform_title = TextMobject("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*map(FadeOutAndShiftDown, basel)),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = TextMobject("This is a grid")
        grid_title.scale(1.5)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title),
            FadeInFromDown(grid_title),
            ShowCreation(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = TextMobject(
            "That was a non-linear function \\\\"
            "applied to the grid"
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.apply_function,
            lambda p: p + np.array([
                np.sin(p[1]),
                np.sin(p[0]),
                0,
            ]),
            run_time=3,
        )
        self.wait()
        self.play(
            Transform(grid_title, grid_transform_title)
        )
        self.wait()


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(ShowCreation(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class WarpSquare(Scene):
    def construct(self):
        square = Square()
        self.play(ApplyPointwiseFunction(
            lambda point: complex_to_R3(np.exp(R3_to_complex(point))),
            square
        ))
        self.wait()


class WriteStuff(Scene):
    def construct(self):
        example_text = TextMobject(
            "This is a some text",
            tex_to_color_map={"text": YELLOW}
        )
        example_tex = TexMobject(
            "\\sum_{k=1}^\\infty {1 \\over k^2} = {\\pi^2 \\over 6}",
        )
        group = VGroup(example_text, example_tex)
        group.arrange(DOWN)
        group.set_width(FRAME_WIDTH - 2 * LARGE_BUFF)

        self.play(Write(example_text))
        self.play(Write(example_tex))
        self.wait()


class UdatersExample(Scene):
    def construct(self):
        decimal = DecimalNumber(
            0,
            show_ellipsis=True,
            num_decimal_places=3,
            include_sign=True,
        )
        square = Square().to_edge(UP)

        decimal.add_updater(lambda d: d.next_to(square, RIGHT))
        decimal.add_updater(lambda d: d.set_value(square.get_center()[1]))
        self.add(square, decimal)
        self.play(
            square.to_edge, DOWN,
            rate_func=there_and_back,
            run_time=5,
        )
        self.wait()

# See old_projects folder for many, many more
