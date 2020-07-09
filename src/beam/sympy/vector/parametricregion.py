from functools import singledispatch
from sympy import pi
from sympy.core import Basic, Tuple
from sympy.core.symbol import _symbol
from sympy.solvers import solve
from sympy.geometry import Point, Segment, Curve, Ellipse, Polygon


class ParametricRegion(Basic):
    """
    Represents a parametric region in space.

    Examples
    ========

    >>> from sympy import cos, sin, pi
    >>> from sympy.abc import r, theta, t, a, b, x, y
    >>> from sympy.vector import ParametricRegion

    >>> ParametricRegion((t, t**2), (t, -1, 2))
    ParametricRegion((t, t**2), (t, -1, 2))
    >>> ParametricRegion((x, y), (x, 3, 4), (y, 5, 6))
    ParametricRegion((x, y), (x, 3, 4), (y, 5, 6))
    >>> ParametricRegion((r*cos(theta), r*sin(theta)), (r, -2, 2), (theta, 0, pi))
    ParametricRegion((r*cos(theta), r*sin(theta)), (r, -2, 2), (theta, 0, pi))
    >>> ParametricRegion((a*cos(t), b*sin(t)), t)
    ParametricRegion((a*cos(t), b*sin(t)), t)

    >>> circle = ParametricRegion((r*cos(theta), r*sin(theta)), r, (theta, 0, pi))
    >>> circle.parameters
    (r, theta)
    >>> circle.definition
    (r*cos(theta), r*sin(theta))
    >>> circle.limits
    {theta: (0, pi)}

    Dimension of a parametric region determines whether a region is a curve, surface
    or volume region. It does not represent its dimensions in space.
    >>> circle.dimensions
    1

    Parameters
    ==========

    definition : tuple to define base scalars in terms of parameters.

    bounds : Parameter or a tuple of length 3 to define parameter and
            corresponding lower and upper bound
    """
    def __new__(cls, definition, *bounds):
        parameters = ()
        limits = {}

        if not isinstance(bounds, Tuple):
            bounds = Tuple(*bounds)

        for bound in bounds:
            if  isinstance(bound, tuple) or isinstance(bound, Tuple):
                if len(bound) != 3:
                    raise ValueError("Tuple should be in the form (parameter, lowerbound, upperbound)")
                parameters += (bound[0],)
                limits[bound[0]] = (bound[1], bound[2])
            else:
                parameters += (bound,)

        if not (isinstance(definition, tuple) or isinstance(definition, Tuple)):
            definition = (definition,)

        obj = super().__new__(cls, Tuple(*definition), *bounds)
        obj._parameters = parameters
        obj._limits = limits

        return obj

    @property
    def definition(self):
        return self.args[0]

    @property
    def limits(self):
        return self._limits

    @property
    def parameters(self):
        return self._parameters

    @property
    def dimensions(self):
        return len(self.limits)


@singledispatch
def parametric_region_list(reg):
    """
    Returns a list of ParametricRegion objects representing the geometric region.

    Examples
    ========

    >>> from sympy.abc import t
    >>> from sympy.vector import parametric_region_list
    >>> from sympy.geometry import Point, Curve, Ellipse, Segment, Polygon

    >>> p = Point(2, 5)
    >>> parametric_region_list(p)
    [ParametricRegion((2, 5))]

    >>> c = Curve((t**3, 4*t), (t, -3, 4))
    >>> parametric_region_list(c)
    [ParametricRegion((t**3, 4*t), (t, -3, 4))]

    >>> e = Ellipse(Point(1, 3), 2, 3)
    >>> parametric_region_list(e)
    [ParametricRegion((2*cos(t) + 1, 3*sin(t) + 3), (t, 0, 2*pi))]

    >>> s = Segment(Point(1, 3), Point(2, 6))
    >>> parametric_region_list(s)
    [ParametricRegion((t + 1, 3*t + 3), (t, 0, 1))]

    >>> p1, p2, p3, p4 = [(0, 1), (2, -3), (5, 3), (-2, 3)]
    >>> poly = Polygon(p1, p2, p3, p4)
    >>> parametric_region_list(poly)
    [ParametricRegion((2*t, 1 - 4*t), (t, 0, 1)), ParametricRegion((3*t + 2, 6*t - 3), (t, 0, 1)),\
     ParametricRegion((5 - 7*t, 3), (t, 0, 1)), ParametricRegion((2*t - 2, 3 - 2*t),  (t, 0, 1))]

    """
    raise ValueError("SymPy cannot determine parametric representation of the region.")


@parametric_region_list.register(Point)
def _(obj):
    return [ParametricRegion(obj.args)]


@parametric_region_list.register(Curve)
def _(obj):
    definition = obj.arbitrary_point(obj.parameter).args
    bounds = obj.limits
    return [ParametricRegion(definition, bounds)]


@parametric_region_list.register(Ellipse)
def _(obj, parameter='t'):
    definition = obj.arbitrary_point(parameter).args
    t = _symbol(parameter, real=True)
    bounds = (t, 0, 2*pi)
    return [ParametricRegion(definition, bounds)]


@parametric_region_list.register(Segment)
def _(obj, parameter='t'):
    t = _symbol(parameter, real=True)
    definition = obj.arbitrary_point(t).args

    for i in range(0, 3):
        lower_bound = solve(definition[i] - obj.points[0].args[i], t)
        upper_bound = solve(definition[i] - obj.points[1].args[i], t)

        if len(lower_bound) == 1 and len(upper_bound) == 1:
            bounds = t, lower_bound[0], upper_bound[0]
            break

    definition_tuple = obj.arbitrary_point(parameter).args
    return [ParametricRegion(definition_tuple, bounds)]


@parametric_region_list.register(Polygon)
def _(obj, parameter='t'):
    l = [parametric_region_list(side, parameter)[0] for side in obj.sides]
    return l
