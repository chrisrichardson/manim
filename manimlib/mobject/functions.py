from manimlib.constants import YELLOW, FRAME_X_RADIUS
import numpy as np
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.mobject.geometry import Dot
from manimlib.utils.config_ops import digest_config


class ParametricFunction(VMobject):
    CONFIG = {
        "t_min": 0,
        "t_max": 1,
        # TODO, be smarter about choosing this number
        "step_size": 0.01,
        "dt": 1e-8,
        # TODO, be smart about figuring these out?
        "discontinuities": [],
        "smoothing": True
    }

    def __init__(self, function, **kwargs):
        self.function = function
        VMobject.__init__(self, **kwargs)

    def get_function(self):
        return self.function

    def get_point_from_function(self, t):
        return self.function(t)

    def generate_points(self):
        t_min, t_max = self.t_min, self.t_max
        dt = self.dt
        step_size = self.step_size

        discontinuities = filter(
            lambda t: t_min <= t <= t_max,
            self.discontinuities
        )
        discontinuities = np.array(list(discontinuities))
        boundary_times = [
            self.t_min, self.t_max,
            *(discontinuities - dt),
            *(discontinuities + dt),
        ]
        boundary_times.sort()
        for t1, t2 in zip(boundary_times[0::2], boundary_times[1::2]):
            t_range = list(np.arange(t1, t2, step_size))
            if t_range[-1] != t2:
                t_range.append(t2)
            points = np.array([self.function(t) for t in t_range])
            valid_indices = np.apply_along_axis(
                np.all, 1, np.isfinite(points)
            )
            points = points[valid_indices]
            if len(points) > 0:
                self.start_new_path(points[0])
                self.add_points_as_corners(points[1:])
        if self.smoothing:
            self.make_smooth()
        return self


class FunctionGraph(ParametricFunction):
    CONFIG = {
        "color": YELLOW,
        "x_min": -FRAME_X_RADIUS,
        "x_max": FRAME_X_RADIUS,
    }

    def __init__(self, function, **kwargs):
        digest_config(self, kwargs)
        self.parametric_function = \
            lambda t: np.array([t, function(t), 0])
        ParametricFunction.__init__(
            self,
            self.parametric_function,
            t_min=self.x_min,
            t_max=self.x_max,
            **kwargs
        )
        self.function = function

    def get_function(self):
        return self.function

    def get_point_from_function(self, x):
        return self.parametric_function(x)


class DiscreteFunction(VMobject):
    CONFIG = {
        "x_min": 0,
        "x_max": 1,
    }

    def __init__(self, values, **kwargs):
        self.values = values
        VMobject.__init__(self, **kwargs)

    def set_values(self, values):
        self.values = values
        self.submobjects = []
        self.generate_points()

    def get_values(self):
        return self.values

    def generate_points(self):
        self.clear_points()
        self.start_new_path(self.values[0])
        self.add_points_as_corners(self.values[1:])

        for p in self.values:
            dot = Dot(p, fill_color=self.color)
            self.add(dot)

        return self
